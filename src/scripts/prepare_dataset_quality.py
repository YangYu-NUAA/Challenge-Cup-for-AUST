#!/usr/bin/env python3
"""Split, enrich and semantically group the government-agent case library."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
GOV_DIR = REPO_ROOT / "data" / "block-01-arbiteros-redteam-rewrite" / "gov_rewrite"
CORE_PATH = GOV_DIR / "arbiteros_cases_gov_rewrite.jsonl"
EXPANDED_PATH = GOV_DIR / "arbiteros_cases_gov_rewrite_expanded.jsonl"
CORE_SPLIT_PATH = GOV_DIR / "core_evaluation_cases.jsonl"
ENHANCED_SPLIT_PATH = GOV_DIR / "enhanced_training_stress_cases.jsonl"
DEDUP_INDEX_PATH = GOV_DIR / "enhanced_semantic_dedup_index.jsonl"
REPORT_PATH = REPO_ROOT / "data" / "_audit" / "dataset_quality_report.md"
REPORT_JSON_PATH = REPO_ROOT / "data" / "_audit" / "dataset_quality_report.json"

SOURCE_METADATA = {
    "Task 1 ArbiterOS 官方": {
        "source_origin": "ArbiterOS official redteam cases",
        "source_license": "Apache-2.0",
    },
    "Task 2 公开数据集": {
        "source_origin": "Agent-SafetyBench / InjecAgent selected public cases",
        "source_license": "MIT; retain per-case upstream attribution",
    },
    "Task 3 原创": {
        "source_origin": "team-authored competition cases",
        "source_license": "team original; explicit redistribution terms pending",
    },
    "Task 4 扩展（OWASP 补充）": {
        "source_origin": "team-generated OWASP-inspired template variants",
        "source_license": "team generated; explicit redistribution terms pending",
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a UTF-8 JSONL file."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write rows as UTF-8 JSONL."""
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def parse_tool_call(call: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    """Return tool name and normalized argument keys."""
    function = call.get("function") if isinstance(call, dict) else None
    if not isinstance(function, dict):
        return "unknown", ()
    name = str(function.get("name") or "unknown").lower()
    arguments = function.get("arguments")
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            arguments = {}
    keys = tuple(sorted(str(key).lower() for key in arguments)) if isinstance(arguments, dict) else ()
    return name, keys


def tool_signature(case: dict[str, Any]) -> list[tuple[str, tuple[str, ...]]]:
    """Collect normalized tool signatures from prior and current steps."""
    signatures: list[tuple[str, tuple[str, ...]]] = []
    messages: list[dict[str, Any]] = []
    for step in case.get("prior") or []:
        if isinstance(step, dict) and isinstance(step.get("message"), dict):
            messages.append(step["message"])
    if isinstance(case.get("current"), dict):
        messages.append(case["current"])
    for message in messages:
        for call in message.get("tool_calls") or []:
            signatures.append(parse_tool_call(call))
    return signatures


def semantic_family_id(case: dict[str, Any]) -> str:
    """Build a path-insensitive structural semantic family identifier."""
    scenario = re.sub(r"（.*?）|\(.*?\)|\d+", "", str(case.get("scenario") or "")).strip()
    canonical = {
        "safe_unsafe": case.get("safe_unsafe"),
        "skill": case.get("skill"),
        "scenario": scenario,
        "tools": tool_signature(case),
    }
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True)
    return "SEM-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12].upper()


def parent_case_id(case: dict[str, Any], core_by_trace: dict[str, str]) -> str | None:
    """Resolve the parent core case or template identifier."""
    trace_id = str(case.get("trace_id") or "")
    source_trace_id = str(case.get("source_trace_id") or "")
    if trace_id in core_by_trace:
        return None
    if source_trace_id in core_by_trace:
        return core_by_trace[source_trace_id]
    case_number = str(case.get("case_number") or "")
    variant_match = re.match(r"^(.+)-V\d+$", case_number, re.I)
    if variant_match:
        return variant_match.group(1)
    new_match = re.match(r"^(NEW-.+)-\d{3}$", case_number, re.I)
    if new_match:
        return new_match.group(1)
    return source_trace_id or None


def enrich_case(
    case: dict[str, Any],
    partition: str,
    core_by_trace: dict[str, str],
) -> dict[str, Any]:
    """Add traceability and review metadata without changing test behavior."""
    enriched = dict(case)
    source = str(case.get("source") or "unknown")
    metadata = SOURCE_METADATA.get(
        source,
        {
            "source_origin": source,
            "source_license": "unknown; manual verification required",
        },
    )
    parent = parent_case_id(case, core_by_trace)
    if partition == "core_evaluation":
        generation_kind = "core"
    elif re.search(r"-V\d+$", str(case.get("case_number") or ""), re.I):
        generation_kind = "path_or_scenario_variant"
    else:
        generation_kind = "new_template_variant"
    enriched.update(
        {
            "dataset_partition": partition,
            "generation_kind": generation_kind,
            "parent_case_id": parent,
            "source_origin": metadata["source_origin"],
            "source_license": metadata["source_license"],
            "human_review_status": "pending_manual_review",
            "semantic_family_id": semantic_family_id(case),
            "semantic_dedup_method": "path-insensitive tool-and-scenario signature v1",
        }
    )
    return enriched


def render_report(summary: dict[str, Any]) -> str:
    """Render the dataset quality report."""
    lines = [
        "# 案例库质量与语义去重报告",
        "",
        "> 本报告区分核心评测案例、跨块映射记录和增强训练/压力测试记录。",
        "",
        "## 统一口径",
        "",
        f"- 核心唯一评测集：{summary['core']['total']} 条（{summary['core']['safe']} safe / {summary['core']['unsafe']} unsafe）。",
        f"- 增强训练/压力测试集：{summary['enhanced']['total']} 条（{summary['enhanced']['safe']} safe / {summary['enhanced']['unsafe']} unsafe）。",
        f"- 全部数据记录：{summary['all_records']} 条，不等于相同数量的独立攻击模式。",
        "- 跨块映射记录：160 条，包含对核心案例的重复引用，不纳入唯一案例数。",
        "",
        "## 语义族去重",
        "",
        f"- 247 条记录归并为 {summary['semantic_families']['all']} 个结构语义族。",
        f"- 167 条增强记录归并为 {summary['semantic_families']['enhanced']} 个结构语义族。",
        f"- 去重索引保留 {summary['dedup_representatives']} 条代表记录，原始增强记录不删除。",
        "- 方法：忽略具体路径、邮箱和数字，只比较 safe/unsafe、Skill、场景主类、工具名和参数键。该方法是启发式语义近似，仍需人工复核。",
        "",
        "## 类别平衡",
        "",
        f"- 增强集 safe 占比：{summary['enhanced']['safe_ratio']:.1%}。",
        f"- 增强集 unsafe 占比：{summary['enhanced']['unsafe_ratio']:.1%}。",
        "- 当前增强集明显偏向 unsafe；在补充困难负样本前，不应将其用于无权重的总体准确率比较。",
        f"- 若以 safe:unsafe 至少 1:2 为目标，现有 {summary['enhanced']['unsafe']} 条 unsafe 至少需要 {summary['balance_gap']['safe_target']} 条 safe；还需补充 {summary['balance_gap']['safe_cases_needed']} 条困难安全案例，或采用分层抽样/类别权重。",
        "- 具体扩充与双人复核要求见 `data/_audit/hard_negative_expansion_plan.md`；计划案例未计入当前数据集。",
        "",
        "## 元数据状态",
        "",
        "每条记录已增加 `source_origin`、`source_license`、`human_review_status`、`parent_case_id`、`dataset_partition`、`generation_kind` 和 `semantic_family_id`。",
        "",
        "> `human_review_status` 统一初始化为 `pending_manual_review`，避免把自动生成或格式校验误写成人工复核通过。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    """Prepare enriched splits and quality reports."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    core = read_jsonl(CORE_PATH)
    expanded = read_jsonl(EXPANDED_PATH)
    core_by_trace = {
        str(case.get("trace_id")): str(case.get("case_number") or case.get("trace_id"))
        for case in core
    }
    core_trace_ids = set(core_by_trace)
    core_rows = [enrich_case(case, "core_evaluation", core_by_trace) for case in core]
    enhanced_source = [
        case for case in expanded if str(case.get("trace_id") or "") not in core_trace_ids
    ]
    enhanced_rows = [
        enrich_case(case, "enhanced_training_stress", core_by_trace)
        for case in enhanced_source
    ]
    all_rows = core_rows + enhanced_rows

    family_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in enhanced_rows:
        family_groups[case["semantic_family_id"]].append(case)
    representatives = [
        sorted(group, key=lambda item: str(item.get("case_number") or ""))[0]
        for group in family_groups.values()
    ]
    representatives.sort(key=lambda item: str(item.get("case_number") or ""))

    core_counts = Counter(case.get("safe_unsafe") for case in core_rows)
    enhanced_counts = Counter(case.get("safe_unsafe") for case in enhanced_rows)
    safe_target = math.ceil(enhanced_counts["unsafe"] / 2)
    summary = {
        "core": {
            "total": len(core_rows),
            "safe": core_counts["safe"],
            "unsafe": core_counts["unsafe"],
        },
        "enhanced": {
            "total": len(enhanced_rows),
            "safe": enhanced_counts["safe"],
            "unsafe": enhanced_counts["unsafe"],
            "safe_ratio": enhanced_counts["safe"] / len(enhanced_rows),
            "unsafe_ratio": enhanced_counts["unsafe"] / len(enhanced_rows),
        },
        "all_records": len(all_rows),
        "semantic_families": {
            "all": len({case["semantic_family_id"] for case in all_rows}),
            "enhanced": len(family_groups),
        },
        "dedup_representatives": len(representatives),
        "balance_gap": {
            "safe_target": safe_target,
            "safe_cases_needed": max(0, safe_target - enhanced_counts["safe"]),
        },
        "largest_enhanced_families": [
            {"semantic_family_id": family_id, "records": len(group)}
            for family_id, group in sorted(
                family_groups.items(), key=lambda item: len(item[1]), reverse=True
            )[:20]
        ],
    }

    if args.write:
        write_jsonl(CORE_PATH, core_rows)
        write_jsonl(EXPANDED_PATH, all_rows)
        write_jsonl(CORE_SPLIT_PATH, core_rows)
        write_jsonl(ENHANCED_SPLIT_PATH, enhanced_rows)
        write_jsonl(DEDUP_INDEX_PATH, representatives)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(render_report(summary), encoding="utf-8")
        REPORT_JSON_PATH.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

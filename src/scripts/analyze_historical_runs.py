#!/usr/bin/env python3
"""Summarize historical 80-case run variability without treating it as controlled repeats."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT.parents[1]
HISTORICAL_ROOT = WORKSPACE_ROOT / "deliverables" / "task5_runs" / "runs"
AUDIT_DIR = REPO_ROOT / "data" / "_audit"


def load_runs() -> list[dict[str, Any]]:
    """Load historical summaries containing exactly 80 cases."""
    runs = []
    for path in sorted(HISTORICAL_ROOT.glob("*/summary.json")):
        summary = json.loads(path.read_text(encoding="utf-8"))
        total = summary.get("total_cases", summary.get("total"))
        if total != 80:
            continue
        runs.append(
            {
                "run_id": summary.get("run_ts") or path.parent.name,
                "path": str(path),
                "passed": summary.get("passed"),
                "failed": summary.get("failed"),
                "results": summary.get("results") or [],
            }
        )
    return runs


def main() -> int:
    """Write compact historical variability evidence."""
    runs = load_runs()
    outcomes: dict[str, list[str]] = defaultdict(list)
    for run in runs:
        by_id = {
            str(result.get("id")): str(result.get("status"))
            for result in run["results"]
        }
        for case_id in sorted(by_id):
            outcomes[case_id].append(by_id[case_id])
    variable = {
        case_id: statuses
        for case_id, statuses in outcomes.items()
        if len(statuses) == len(runs) and len(set(statuses)) > 1
    }
    report = {
        "scope": "historical debugging runs; not controlled repetitions",
        "runs": [
            {
                "run_id": run["run_id"],
                "passed": run["passed"],
                "failed": run["failed"],
            }
            for run in runs
        ],
        "variable_case_count": len(variable),
        "variable_cases": variable,
    }
    lines = [
        "# 历史批跑波动分析",
        "",
        "> 下列批次来自开发调试过程，未完整记录 commit、配置哈希和受控变量，不能当作正式重复实验；仅用于证明结果存在版本/配置波动。",
        "",
        "| 批次 | 通过 | 失败 | 通过率 |",
        "|---|---:|---:|---:|",
    ]
    for run in report["runs"]:
        total = int(run["passed"] or 0) + int(run["failed"] or 0)
        rate = (int(run["passed"] or 0) / total) if total else 0.0
        lines.append(
            f"| {run['run_id']} | {run['passed']} | {run['failed']} | {rate:.1%} |"
        )
    lines.extend(
        [
            "",
            f"- 三批 80 条运行中共有 {len(variable)} 条案例的 pass/fail 发生变化。",
            "- 正式性能结论以 `experiment_metrics.md` 的 5×80 受控重复实验为准。",
            "",
            "## 波动案例",
            "",
            "| case_id | 依时间顺序的结果 |",
            "|---|---|",
        ]
    )
    for case_id, statuses in sorted(variable.items()):
        lines.append(f"| {case_id} | {' → '.join(statuses)} |")
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    (AUDIT_DIR / "historical_run_variability.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (AUDIT_DIR / "historical_run_variability.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

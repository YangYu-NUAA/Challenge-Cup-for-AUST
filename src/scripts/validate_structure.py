#!/usr/bin/env python3
"""
仓库结构与交付物自检脚本（按任务书）
用法：
  python src/scripts/validate_structure.py          # 模板模式：只看结构/元数据
  python src/scripts/validate_structure.py --strict # 严格模式：要求交付物非空
"""

from pathlib import Path
import json
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"

# 每块必须存在的文件（相对块目录）；strict 模式下还要求非空
BLOCK_REQUIREMENTS = {
    "block-01-arbiteros-redteam-rewrite": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "human_readable/arbiteros_cases_human_readable.xlsx",
            "gov_rewrite/arbiteros_cases_gov_rewrite.jsonl",
            "arbiteros_case_source_index.md",
        ],
        "metadata_title": "ArbiterOS 红队案例提取与政务改写",
    },
    "block-02-public-datasets-attack-patterns": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "screening/public_benchmark_case_screening.xlsx",
            "gov_cases/public_patterns_to_gov_cases.jsonl",
            "discarded/discarded_cases.md",
        ],
        "metadata_title": "公开数据集与安全标准中的攻击模式提取",
    },
    "block-03-gov-original-skills": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "skills/gov-meeting-assistant/SKILL.md",
            "skills/gov-document-assistant/SKILL.md",
            "skills/gov-mail-assistant/SKILL.md",
            "skills/gov-calendar-task-assistant/SKILL.md",
            "skills/gov-cross-department-assistant/SKILL.md",
            "cases/gov_original_cases.jsonl",
        ],
        "metadata_title": "政务办公原创场景与 OpenClaw 办公 Skills",
    },
    "block-04-risk-grading-policy": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "risk_level_matrix.xlsx",
            "policy/gov_policy_rules.yaml",
            "case_to_policy_mapping.xlsx",
        ],
        "metadata_title": "四级风险分级与策略规则",
    },
    "block-05-arbiteros-batch-run": {
        "required_files": [
            "README.md",
            "metadata.yml",
            "index/arbiteros_run_index.xlsx",
            "notes/arbiteros_failure_notes.md",
            "notes/arbiteros_result_summary.md",
        ],
        "metadata_title": "ArbiterOS 既有案例批跑与结果归档",
    },
    "system-design": {
        "required_files": ["README.md", "metadata.yml"],
        "metadata_title": "总框架接入与系统设计（维护者）",
    },
}

METADATA_KEYS = ["block", "title", "person", "collection_date", "status", "sources", "deliverables"]


def validate_jsonl(path: Path) -> list[str]:
    """Validate that a JSONL deliverable has parseable rows."""
    errors: list[str] = []
    rows = 0
    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rows += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: 第 {line_no} 行不是合法 JSON: {exc}")
            continue
        row_id = str(row.get("case_number") or row.get("trace_id") or row.get("id") or "")
        if row_id:
            if row_id in seen_ids:
                duplicate_ids.add(row_id)
            seen_ids.add(row_id)
    if rows == 0:
        errors.append(f"{path}: JSONL 没有数据行")
    if duplicate_ids:
        errors.append(f"{path}: 存在重复编号 {sorted(duplicate_ids)[:5]}")
    return errors


def validate_xlsx(path: Path) -> list[str]:
    """Validate that an XLSX deliverable contains at least one data row."""
    try:
        import openpyxl
    except ImportError:
        return [f"{path}: 未安装 openpyxl，无法检查 Excel 数据行"]

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    data_rows = 0
    for ws in wb.worksheets:
        nonempty_rows = 0
        for row in ws.iter_rows(values_only=True):
            if any(cell is not None for cell in row):
                nonempty_rows += 1
        data_rows += max(0, nonempty_rows - 1)
    if data_rows == 0:
        return [f"{path}: Excel 只有表头或为空"]
    return []


def validate_standard_cases() -> list[str]:
    """Validate the unified ArbiterOS case library."""
    errors: list[str] = []
    base = DATA_DIR / "arbiteros_standard_cases"
    manifest_path = base / "gov_office_case_manifest.json"
    if not manifest_path.exists():
        return ["缺少统一案例库 manifest: data/arbiteros_standard_cases/gov_office_case_manifest.json"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{manifest_path}: 不是合法 JSON: {exc}"]

    case_files = sorted(base.glob("*/*.json"))
    manifest_cases = manifest.get("cases", [])
    if manifest.get("total") != len(case_files):
        errors.append(f"统一案例库 total={manifest.get('total')}，实际文件数={len(case_files)}")
    if isinstance(manifest_cases, list) and len(manifest_cases) != len(case_files):
        errors.append(f"统一案例库 manifest cases={len(manifest_cases)}，实际文件数={len(case_files)}")

    for case_path in case_files:
        try:
            case = json.loads(case_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{case_path}: 不是合法 JSON: {exc}")
            continue
        for key in ("trace_id", "prior", "current"):
            if key not in case:
                errors.append(f"{case_path}: 缺少 {key}")
        current = case.get("current") or {}
        if "tool_calls" not in current and "content" not in current:
            errors.append(f"{case_path}: current 缺少 tool_calls 或 content")
    return errors


def validate_block(name: str, spec: dict, strict: bool):
    errors, warnings = [], []
    block_dir = DATA_DIR / name
    if not block_dir.is_dir():
        errors.append(f"目录缺失: data/{name}")
        return errors, warnings

    for rel in spec["required_files"]:
        f = block_dir / rel
        if not f.exists():
            errors.append(f"缺少文件: data/{name}/{rel}")
        elif strict and f.stat().st_size == 0:
            # 模板生成的示例 jsonl/xlsx 已有内容，空文件视为未填写
            warnings.append(f"文件为空，请填写: data/{name}/{rel}")
        elif strict and f.suffix == ".jsonl":
            errors.extend(validate_jsonl(f))
        elif strict and f.suffix == ".xlsx":
            errors.extend(validate_xlsx(f))

    meta = block_dir / "metadata.yml"
    if meta.exists():
        try:
            text = meta.read_text(encoding="utf-8")
            for key in METADATA_KEYS:
                if not re.search(rf"^{re.escape(key)}:\s", text, re.MULTILINE):
                    errors.append(f"metadata.yml 缺少字段: {key}")
            if strict and name != "system-design" and 'used: false' in text:
                warnings.append("metadata.yml 中 ai_assistance.used 仍为 false，如已用 AI 请更新")
        except Exception as e:
            errors.append(f"metadata.yml 读取失败: {e}")
    return errors, warnings


def main():
    strict = "--strict" in sys.argv
    print("=" * 64)
    print(f"仓库结构自检（{'严格模式' if strict else '模板模式'}）")
    print("=" * 64)
    all_ok = True
    for name, spec in BLOCK_REQUIREMENTS.items():
        errors, warnings = validate_block(name, spec, strict)
        print(f"\n[{name}]")
        if errors:
            all_ok = False
            for e in errors:
                print(f"  ❌ {e}")
        if warnings:
            for w in warnings:
                print(f"  ⚠️  {w}")
        if not errors and not warnings:
            print("  ✅ 通过")
    if strict:
        print("\n[arbiteros_standard_cases]")
        case_errors = validate_standard_cases()
        if case_errors:
            all_ok = False
            for e in case_errors:
                print(f"  ❌ {e}")
        else:
            print("  ✅ 通过")
    print("\n" + "=" * 64)
    print("✅ 结构检查通过（无阻塞错误）" if all_ok else "❌ 存在阻塞错误，请按提示补充")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

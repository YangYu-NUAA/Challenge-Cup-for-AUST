"""Convert 160 cases from block-01/02/03 JSONL into ArbiterOS standard
directory layout (`redteam/case/<scenario>/<case_id>.json`).

Output: data/arbiteros_standard_cases/<skill>/<case_id>.json
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data" / "arbiteros_standard_cases"

SOURCES = [
    ("block-01", REPO / "data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl"),
    ("block-02", REPO / "data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl"),
    ("block-03", REPO / "data/block-03-gov-original-skills/cases/gov_original_cases.jsonl"),
]


def convert(case: dict) -> dict:
    """Drop non-ArbiterOS wrapper fields, keep trace_id / prior / current."""
    out = {
        "trace_id": case["trace_id"],
        "prior": case.get("prior", []),
        "current": case["current"],
    }
    # Preserve tag structure (current.tag, plus tags inside each prior entry)
    # Ensure each prior entry has tag field (some may not)
    for step in out["prior"]:
        step.setdefault("tag", {})
    out["current"].setdefault("tag", {})
    return out


def main() -> None:
    # Clean output
    if OUT.exists():
        for p in OUT.rglob("*"):
            if p.is_file():
                p.unlink()
        for p in sorted(OUT.rglob("*"), reverse=True):
            if p.is_dir():
                p.rmdir()
    else:
        OUT.mkdir(parents=True)

    count_by_skill: dict[str, int] = {}
    written = 0
    errors = []

    for block, path in SOURCES:
        if not path.exists():
            errors.append(f"MISSING: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    case = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"{path}:{lineno} JSON parse error: {e}")
                    continue

                skill = case.get("skill", "unknown")
                case_id = case.get("case_number") or case.get("trace_id", f"unknown-{lineno}")
                out_dir = OUT / skill
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file = out_dir / f"{case_id}.json"

                # Sanity check: no overwrite of same case_id from different blocks
                if out_file.exists():
                    existing = json.loads(out_file.read_text(encoding="utf-8"))
                    if existing.get("trace_id") != case.get("trace_id"):
                        errors.append(f"DUPLICATE case_id across blocks: {case_id}")

                out_file.write_text(
                    json.dumps(convert(case), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                count_by_skill[skill] = count_by_skill.get(skill, 0) + 1
                written += 1

    # Write README for the library
    readme = OUT / "README.md"
    lines = [
        "# ArbiterOS 标准案例库",
        "",
        "> 从 block-01/02/03 汇总的 160 条案例，按 Skill 分组，可直接复制到",
        "> `ArbiterOS-Kernel/redteam/case/<scenario>/` 下批量运行。",
        "",
        "## 目录",
        "",
    ]
    for skill in sorted(count_by_skill):
        lines.append(f"- `{skill}/` — {count_by_skill[skill]} 条")
    lines += [
        "",
        f"共 {written} 条案例。",
        "",
        "## 使用方式",
        "",
        "```bash",
        "# 复制到 ArbiterOS-Kernel",
        "cp -r data/arbiteros_standard_cases/<skill> ArbiterOS-Kernel/redteam/case/<scenario>/",
        "",
        "# 生成 manifest 后批量运行",
        "cd ArbiterOS-Kernel",
        "uv run python redteam/_automation/run_cases.py --kind all --manifest <manifest.json>",
        "```",
        "",
        "## 来源",
        "",
        "- `block-01`：80 条政务改写（Task 1 原始 30 + Task 2 公开 27 + Task 3 原创 23）",
        "- `block-02`：27 条公开数据集（Agent-SafetyBench + InjecAgent）",
        "- `block-03`：53 条原创政务场景（5 个 Skill）",
        "",
    ]
    if errors:
        lines += ["## 错误\n", "\n".join(f"- {e}" for e in errors)]

    readme.write_text("\n".join(lines), encoding="utf-8")

    print(f"Written {written} cases to {OUT}")
    for skill, n in sorted(count_by_skill.items()):
        print(f"  {skill}: {n}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors[:10]:
            print(f"  {e}")
    else:
        print("No errors.")


if __name__ == "__main__":
    main()

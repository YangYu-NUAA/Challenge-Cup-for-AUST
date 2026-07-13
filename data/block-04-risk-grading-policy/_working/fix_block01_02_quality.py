"""Fix block-01/02 case quality issues:
- block-01: 27 PUB-* cases missing skill + case_type (foreign keys from block-02)
- block-02: all 27 cases missing skill + case_type

Strategy: fill missing fields from scenario text using keyword matching.
Leave block-03 untouched (already clean).
"""

from __future__ import annotations

import json, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

SCENARIO_TO_SKILL = [
    (re.compile(r"邮件|mail|email|e-mail", re.I), "gov-mail-assistant"),
    (re.compile(r"文档|文件|document|file", re.I), "gov-document-assistant"),
    (re.compile(r"会议|日程|calendar|schedule|meeting", re.I), "gov-calendar-task-assistant"),
    (re.compile(r"跨部门|知识库|kb|知识|collaborat|知识库", re.I), "gov-cross-department-assistant"),
    (re.compile(r"门禁|权限|lock|access|门禁", re.I), "gov-cross-department-assistant"),
    (re.compile(r"短信|sms|消息|message", re.I), "gov-mail-assistant"),
    (re.compile(r"任务|task|todo", re.I), "gov-calendar-task-assistant"),
    (re.compile(r"浏览器|browser|web|导航|navigate", re.I), "gov-cross-department-assistant"),
    (re.compile(r"浏览器|browser|web|导航|navigate", re.I), "gov-cross-department-assistant"),
]

DEFAULT_SKILL = "gov-cross-department-assistant"


def guess_skill(scenario: str) -> str:
    for pat, skill in SCENARIO_TO_SKILL:
        if pat.search(scenario):
            return skill
    return DEFAULT_SKILL


def fix_block(jsonl_path: Path, block_name: str) -> dict:
    lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    cases = [json.loads(l) for l in lines if l.strip()]

    fixed_skill = 0
    fixed_case_type = 0
    examples = []

    for c in cases:
        cid = c.get("case_number") or c.get("trace_id", "?")
        scenario = c.get("scenario", "")

        if not c.get("skill"):
            c["skill"] = guess_skill(scenario)
            fixed_skill += 1
            if len(examples) < 5:
                examples.append(f"  {cid}: skill={c['skill']} (from scenario: {scenario[:40]})")

        if not c.get("case_type"):
            c["case_type"] = "attack"
            fixed_case_type += 1

    # Write back
    jsonl_path.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in cases) + "\n",
        encoding="utf-8",
    )

    print(f"\n[{block_name}] {jsonl_path.name}")
    print(f"  Fixed skill: {fixed_skill}, fixed case_type: {fixed_case_type}")
    for ex in examples:
        print(ex)
    return {"fixed_skill": fixed_skill, "fixed_case_type": fixed_case_type, "total": len(cases)}


def main() -> None:
    results = []
    for block, rel in [
        ("block-01", REPO / "data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl"),
        ("block-02", REPO / "data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl"),
    ]:
        if rel.exists():
            results.append((block, fix_block(rel, block)))

    # Re-validate
    print("\n=== POST-FIX VALIDATION ===")
    for block, rel in [
        ("block-01", REPO / "data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl"),
        ("block-02", REPO / "data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl"),
    ]:
        if not rel.exists():
            continue
        cases = [json.loads(l) for l in rel.read_text(encoding='utf-8').splitlines() if l.strip()]
        missing = [(c.get('case_number','?'), k) for c in cases for k in ['skill','case_type'] if not c.get(k)]
        print(f"[{block}] {len(cases)} cases, missing skill/case_type: {len(missing)}")
        if missing[:3]:
            for cid, k in missing[:3]:
                print(f"    - {cid} missing {k}")


if __name__ == "__main__":
    main()

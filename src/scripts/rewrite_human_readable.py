#!/usr/bin/env python3
# coding: utf-8
"""
把 block-01 的人类可读记录 *.md 按 jsonl 权威源批量重写为自然语言。
用法：python src/scripts/rewrite_human_readable.py [--apply]
默认只生成到 _preview/ 供检查；加 --apply 才覆盖 human_readable/。
"""
import json, re, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCK = ROOT / "data/block-01-arbiteros-redteam-rewrite"
SRC = BLOCK / "gov_rewrite/arbiteros_cases_gov_rewrite.jsonl"
HUMAN = BLOCK / "human_readable"

SRC_MAP = {
    "Task 1 ArbiterOS 官方": "1 号 ArbiterOS 官方",
    "Task 2 公开数据集": "2 号公开数据集",
    "Task 3 原创": "3 号原创",
}

# 每个 skill 的正常能力白话（正常任务用）
SKILL_NORMAL = {
    "gov-meeting-assistant": "总结会议纪要、提取待办、生成会议通知草稿",
    "gov-document-assistant": "总结政策文件、提取条款、生成汇报草稿",
    "gov-mail-assistant": "分类与摘要邮件、起草回复草稿",
    "gov-calendar-task-assistant": "起草会议邀请、提取任务、生成提醒",
    "gov-cross-department-assistant": "生成协同单、查询 mock 部门资料、整理流程状态",
}
DEFAULT_NORMAL = "按对应办公 Skill 的正常流程处理用户请求"


def parse_args(s):
    try:
        return json.loads(s)
    except Exception:
        return {}


def desc_tool_call(tc):
    if not tc:
        return "（无工具调用，纯文本回复）"
    fn = tc.get("function", {})
    name = fn.get("name", "?")
    a = parse_args(fn.get("arguments", "{}"))
    a = {k: v for k, v in a.items() if k != "reference_tool_id"}

    def short(v, n=40):
        s = str(v)
        return s if len(s) <= n else s[:n] + "…"

    if name in ("send_email", "send_email_batch"):
        to = a.get("to")
        if isinstance(to, list):
            to = "、".join(to)
        return f"发送邮件（收件人：{short(to)}；主题：{short(a.get('subject',''))}）"
    if name in ("read",):
        return f"读取文件（{short(a.get('path') or a.get('file_path'))}）"
    if name in ("write", "file_write", "save"):
        return f"写入文件（{short(a.get('path') or a.get('file_path'))}）"
    if name in ("exec",):
        return f"执行命令（{short(a.get('command'))}）"
    if name in ("calendar_list_events",):
        return f"查询日程（{a.get('start','')}~{a.get('end','')}）"
    if name in ("calendar.create", "create_event"):
        return f"创建日程（{short(a.get('subject') or a.get('title',''))}）"
    if name in ("kb_search", "search"):
        return f"查询知识库（{short(a.get('query') or a.get('keyword',''))}）"
    if name in ("delete", "file_delete"):
        return f"删除文件（{short(a.get('path'))}）"
    parts = "；".join(f"{k}={short(v)}" for k, v in a.items())
    return f"{name}（{parts}）" if parts else name


def scene_inner(scenario):
    m = re.search(r"（(.+)）", scenario or "")
    return m.group(1) if m else (scenario or "")


def normal_task(row):
    skill = row.get("skill")
    base = SKILL_NORMAL.get(skill, DEFAULT_NORMAL)
    if row.get("case_type") == "normal" or row.get("safe_unsafe") == "safe":
        return f"{base}。本条为正常用例。"
    return base + "。"


def malicious_goal(row):
    if row.get("safe_unsafe") == "safe":
        return "无（本条为正常任务）"
    cur = row.get("current", {})
    tcs = cur.get("tool_calls") or []
    acts = "；".join(desc_tool_call(tc) for tc in tcs) or "执行了不被允许的动作"
    inner = scene_inner(row.get("scenario", ""))
    return f"在【{inner}】场景下，智能体被诱导执行：{acts}。"


def expected(row):
    """预期防护由 4 号风险分级回填，先留锚点。safe 仍可安全写允许。"""
    if row.get("safe_unsafe") == "safe":
        return "允许正常执行；记录审计日志。\n> TODO(4号回填)：本条为 safe，默认低风险；待 4 号最终确认。"
    return "> TODO(4号回填)：风险等级待定（低/中/高/默认阻断）；决策待定（allow/log/approval/deny）。"


AUDIT = "输入来源、风险标签、触发动作、命中策略、系统决策、证据摘要"


def render(row):
    cn = row.get("case_number", "")
    scenario = row.get("scenario", "")
    src = SRC_MAP.get(row.get("source", ""), row.get("source", ""))
    ct = row.get("case_type") or ("normal" if row.get("safe_unsafe") == "safe" else "attack")
    danger = ("；".join(desc_tool_call(tc) for tc in (row.get("current", {}).get("tool_calls") or []))) or "（无）"
    return f"""# {cn}

- **案例编号**：{cn}
- **来源**：{src}
- **政务场景**：{scenario}
- **safe/unsafe**：{row.get('safe_unsafe', '')}
- **case_type**：{ct}

## 正常任务

{normal_task(row)}

## 恶意目标

{malicious_goal(row)}

## 危险工具动作

{danger}

## 预期防护

{expected(row)}

## 审计记录点

{AUDIT}

---
"""


def main():
    apply = "--apply" in sys.argv
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
    out_dir = HUMAN if apply else (BLOCK / "_preview")
    if not apply:
        out_dir.mkdir(exist_ok=True)
    n = 0
    for row in rows:
        (out_dir / f"{row['case_number']}.md").write_text(render(row), encoding="utf-8")
        n += 1
    print(f"已生成 {n} 个 md → {out_dir}")
    if not apply:
        print("确认无误后，加 --apply 覆盖 human_readable/")


if __name__ == "__main__":
    main()

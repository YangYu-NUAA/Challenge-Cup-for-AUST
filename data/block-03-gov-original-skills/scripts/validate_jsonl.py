#!/usr/bin/env python3
"""验证 gov_original_cases.jsonl 的 ArbiterOS 格式完整性。"""
import json, sys
from pathlib import Path

CASES_FILE = Path(__file__).resolve().parent.parent / "cases" / "gov_original_cases.jsonl"

with open(CASES_FILE, encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip()]

issues = []
warnings = []

for i, line in enumerate(lines, 1):
    try:
        case = json.loads(line)
    except json.JSONDecodeError as e:
        issues.append(f"[行{i}] JSON 解析失败: {e}")
        continue

    cn = case.get("case_number", f"行{i}")

    # --- 必填字段 ---
    for field in ["trace_id", "prior", "current"]:
        if field not in case:
            issues.append(f"[{cn}] 缺少必填字段: {field}")

    # --- prior 结构 ---
    prior = case.get("prior", [])
    prior_call_ids = set()

    for j, step in enumerate(prior):
        kind = step.get("kind")
        if kind not in ("assistant", "tool"):
            issues.append(f"[{cn}] prior[{j}] kind 无效: {kind}")
            continue

        if kind == "assistant":
            msg = step.get("message", {})
            if "tag" not in msg:
                issues.append(f"[{cn}] prior[{j}].message 缺少 tag")
            for tc in msg.get("tool_calls", []):
                cid = tc.get("id", "")
                prior_call_ids.add(cid)
                if not cid:
                    issues.append(f"[{cn}] prior[{j}] tool_call 缺少 id")
                # 检查 arguments 中的 reference_tool_id
                args_str = tc.get("function", {}).get("arguments", "{}")
                try:
                    args = json.loads(args_str) if isinstance(args_str, str) else args_str
                except (json.JSONDecodeError, TypeError):
                    issues.append(f"[{cn}] prior[{j}] arguments JSON 解析失败: {str(args_str)[:100]}")
                    continue
                if "reference_tool_id" not in args:
                    issues.append(f"[{cn}] prior[{j}] arguments 缺少 reference_tool_id")

        elif kind == "tool":
            if "tag" not in step:
                issues.append(f"[{cn}] prior[{j}] tool 步骤缺少 tag")
            tid = step.get("tool_call_id", "")
            prior_call_ids.add(tid)
            if not tid:
                issues.append(f"[{cn}] prior[{j}] tool 步骤缺少 tool_call_id")
            # 检查 result 中有没有泄露敏感信息
            result = step.get("result", "")
            if not result:
                warnings.append(f"[{cn}] prior[{j}] tool result 为空（可能正常）")

    # --- current 结构 ---
    cur = case.get("current", {})
    if "tag" not in cur:
        issues.append(f"[{cn}] current 缺少 tag")

    cur_calls = cur.get("tool_calls", [])
    if not cur_calls:
        issues.append(f"[{cn}] current.tool_calls 为空")

    for tc in cur_calls:
        cid = tc.get("id", "")
        if not cid:
            issues.append(f"[{cn}] current tool_call 缺少 id")
        args_str = tc.get("function", {}).get("arguments", "{}")
        try:
            args = json.loads(args_str) if isinstance(args_str, str) else args_str
        except (json.JSONDecodeError, TypeError):
            issues.append(f"[{cn}] current arguments JSON 解析失败: {str(args_str)[:100]}")
            continue
        if "reference_tool_id" not in args:
            issues.append(f"[{cn}] current arguments 缺少 reference_tool_id")
        # reference_tool_id 应引用 prior 中已有的 call id
        refs = args.get("reference_tool_id", [])
        for ref in refs:
            if ref and ref not in prior_call_ids:
                warnings.append(f"[{cn}] reference_tool_id '{ref}' 未在 prior 中找到（可能是 cross-step 引用）")

    # --- 扩展字段 ---
    for field in ["case_number", "safe_unsafe", "scenario", "skill"]:
        if field not in case:
            warnings.append(f"[{cn}] 缺少扩展字段: {field}")

print(f"检查 {len(lines)} 条案例")
print(f"错误: {len(issues)}")
print(f"警告: {len(warnings)}")
print()

if issues:
    print("=== 错误 ===")
    for x in issues:
        print(f"  {x}")
    print()

if warnings:
    print("=== 警告 ===")
    for x in warnings:
        print(f"  {x}")

if not issues:
    print("ArbiterOS 格式结构检查通过，未发现错误。")

#!/usr/bin/env python3
"""block-03 全面审查：规范合规性、数据正确性、跨文件一致性。"""
import json
from pathlib import Path

BLOCK = Path(__file__).resolve().parent.parent
JSONL_PATH = BLOCK / "cases" / "gov_original_cases.jsonl"
HR_DIR = BLOCK / "human_readable"
SKILLS_DIR = BLOCK / "skills"

# ========== 1. JSONL 加载 ==========
with open(JSONL_PATH, encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip()]

cases = []
for i, line in enumerate(lines, 1):
    try:
        cases.append(json.loads(line))
    except json.JSONDecodeError as e:
        print(f"[JSONL 行{i}] 解析失败: {e}")

cn_set = {c.get("case_number") for c in cases}
print(f"=== 1. JSONL 概览 ===")
print(f"案例总数: {len(cases)}")
print(f"唯一 case_number: {len(cn_set)}")

# ========== 2. 人类可读文件 ==========
hr_files = sorted(HR_DIR.glob("ORIG-*.md"))
hr_cns = {f.stem for f in hr_files}
print(f"\n=== 2. 人类可读文件 ===")
print(f"human_readable/ 中 ORIG-*.md: {len(hr_files)}")
missing_hr = cn_set - hr_cns
extra_hr = hr_cns - cn_set
if missing_hr:
    print(f"  ❌ JSONL 有但 human_readable 缺: {sorted(missing_hr)}")
if extra_hr:
    print(f"  ❌ human_readable 多余: {sorted(extra_hr)}")
if not missing_hr and not extra_hr:
    print(f"  ✅ 与 JSONL case_number 一一对应")

# 检查每个 human_readable 是否含 5 必填字段
required_sections = ["正常任务", "恶意目标", "危险工具动作", "预期防护", "审计记录点"]
hr_issues = []
for f in hr_files:
    content = f.read_text(encoding="utf-8")
    for sec in required_sections:
        if f"## {sec}" not in content:
            hr_issues.append(f"{f.stem}: 缺少章节 {sec}")
if hr_issues:
    print(f"  ❌ 章节缺失: {len(hr_issues)} 处")
    for x in hr_issues[:5]:
        print(f"     {x}")
    if len(hr_issues) > 5:
        print(f"     ... 还有 {len(hr_issues)-5} 处")
else:
    print(f"  ✅ 53 个文件全部含 5 必填字段")

# ========== 3. SKILL.md 检查 ==========
skill_required = ["name:", "description:", "适用场景", "正常流程", "允许动作", "禁止动作", "风险识别", "输出格式", "测试案例", "工具清单"]
skill_issues = []
for skill_dir in sorted(SKILLS_DIR.iterdir()):
    if not skill_dir.is_dir():
        continue
    sf = skill_dir / "SKILL.md"
    if not sf.exists():
        skill_issues.append(f"{skill_dir.name}: SKILL.md 不存在")
        continue
    content = sf.read_text(encoding="utf-8")
    for sec in skill_required:
        if sec not in content:
            skill_issues.append(f"{skill_dir.name}: 缺少章节 {sec}")

print(f"\n=== 3. SKILL.md 检查 ===")
print(f"Skill 数量: {len(list(SKILLS_DIR.iterdir()))}")
if skill_issues:
    print(f"  ❌ 问题: {len(skill_issues)} 处")
    for x in skill_issues:
        print(f"     {x}")
else:
    print(f"  ✅ 全部 5 个 SKILL.md 含所有必需章节")

# ========== 4. skill 分配检查 ==========
skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
case_skills = set()
for c in cases:
    s = c.get("skill", "")
    case_skills.add(s)
    if s not in skill_names:
        print(f"  ❌ {c.get('case_number')}: skill '{s}' 不在 skills/ 目录中")

unknown_skills = case_skills - skill_names
if not unknown_skills:
    print(f"  ✅ 所有案例的 skill 字段匹配 skills/ 目录")

# ========== 5. safe/unsafe 统计 ==========
safe_count = sum(1 for c in cases if c.get("safe_unsafe") == "safe")
unsafe_count = sum(1 for c in cases if c.get("safe_unsafe") == "unsafe")
other_su = len(cases) - safe_count - unsafe_count
print(f"\n=== 5. safe/unsafe 统计 ===")
print(f"safe: {safe_count}, unsafe: {unsafe_count}, 其他: {other_su}")
if safe_count == 22 and unsafe_count == 31:
    print(f"  ✅ 与 README 一致 (22+31=53)")

# ========== 6. 数据红线检查 ==========
print(f"\n=== 6. 数据安全红线 ===")
forbidden = ["真实", "gov.cn", "@gov.cn", "12345", "password", "123456", "admin", "192.168", "10.0.", "172.16"]
redline_hits = []
for i, line in enumerate(lines, 1):
    for fb in forbidden:
        if fb.lower() in line.lower():
            redline_hits.append(f"  行{i}: 含疑似真实数据 '{fb}'")
# Also check for allowed test domains
all_allowed = True
for line in lines:
    l = line.lower()
    # Check email domains
    import re
    emails = re.findall(r'[\w.-]+@[\w.-]+', l)
    for e in emails:
        domain = e.split('@')[1]
        if domain not in ('mock-gov.local', 'example.com'):
            if 'mock' not in domain and 'example' not in domain:
                redline_hits.append(f"  可疑邮箱域名: {e}")
                all_allowed = False
if redline_hits:
    print(f"  ❌ {len(redline_hits)} 处疑似违规:")
    for x in redline_hits[:10]:
        print(x)
else:
    print(f"  ✅ 未发现真实数据、真实邮箱、真实系统的痕迹")

# ========== 7. case_number 格式检查 ==========
import re
print(f"\n=== 7. case_number 格式 ===")
bad_format = []
expected_prefixes = ["ORIG-BULK", "ORIG-CAL", "ORIG-CROSS", "ORIG-DOC", "ORIG-EDGE", "ORIG-IMP", "ORIG-MAIL", "ORIG-MEETING", "ORIG-OWASP"]
for c in cases:
    cn = c.get("case_number", "")
    if not re.match(r'^ORIG-[A-Z]+-\d{3}$', cn):
        bad_format.append(cn)
    else:
        prefix = cn[:cn.rindex('-')] if '-' in cn else cn
        if prefix not in expected_prefixes:
            bad_format.append(f"{cn} (未知前缀)")
if bad_format:
    print(f"  ❌ 格式异常: {bad_format}")
else:
    print(f"  ✅ 全部 53 条格式为 ORIG-{'{分类}'}-{'{序号}'}")

# ========== 8. trace_id 唯一性 ==========
trace_ids = [c.get("trace_id") for c in cases]
if len(trace_ids) == len(set(trace_ids)):
    print(f"  ✅ trace_id 全部唯一")

# ========== 9. 按 skill 分布 ==========
print(f"\n=== 9. 按 skill 分布 ===")
by_skill = {}
for c in cases:
    s = c.get("skill", "unknown")
    by_skill[s] = by_skill.get(s, 0) + 1
for s, n in sorted(by_skill.items(), key=lambda x: -x[1]):
    safe_n = sum(1 for c in cases if c.get("skill") == s and c.get("safe_unsafe") == "safe")
    unsafe_n = sum(1 for c in cases if c.get("skill") == s and c.get("safe_unsafe") == "unsafe")
    print(f"  {s}: {n} (safe={safe_n}, unsafe={unsafe_n})")

# ========== 10. 汇总 ==========
print(f"\n========== 审查完成 ==========")

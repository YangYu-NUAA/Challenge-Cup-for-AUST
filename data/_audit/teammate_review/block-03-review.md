# Block 03 复核指南（3 号负责人）

> 复核人：_______  日期：_______

---

## 本块交付物清单

| 文件 | 说明 | 应存在？ |
|------|------|----------|
| `data/block-03-gov-original-skills/cases/gov_original_cases.jsonl` | 53 条原创案例 | ✅ |
| `data/block-03-gov-original-skills/skills/gov-meeting-assistant/SKILL.md` | 会议助手 Skill | ✅ |
| `data/block-03-gov-original-skills/skills/gov-document-assistant/SKILL.md` | 文档助手 Skill | ✅ |
| `data/block-03-gov-original-skills/skills/gov-mail-assistant/SKILL.md` | 邮件助手 Skill | ✅ |
| `data/block-03-gov-original-skills/skills/gov-calendar-task-assistant/SKILL.md` | 日程任务助手 Skill | ✅ |
| `data/block-03-gov-original-skills/skills/gov-cross-department-assistant/SKILL.md` | 跨部门助手 Skill | ✅ |
| `data/block-03-gov-original-skills/metadata.yml` | 块元数据 | ✅ |
| `data/block-03-gov-original-skills/README.md` | 块说明 | ✅ |

> **注意**：block-01 已合并本块 53 条案例（23 条 ORIG-* 原创 + 30 条官方 = 80 条唯一案例）。block-03 的 `gov_original_cases.jsonl` 是原始存储。

---

## 验证步骤

### 1. 案例 JSONL 验证

```bash
python -X utf8 -c "
import json
from pathlib import Path
path = Path('data/block-03-gov-original-skills/cases/gov_original_cases.jsonl')
cases = [json.loads(l) for l in path.read_text(encoding='utf-8').strip().split('\n') if l.strip()]
print(f'案例总数: {len(cases)}')

# 必填字段
required = ['trace_id', 'prior', 'current', 'case_number', 'safe_unsafe', 'scenario', 'skill']
for field in required:
    missing = [c.get('case_number','?') for c in cases if field not in c]
    print(f'缺少 {field}: {len(missing)}')

# safe/unsafe 分布
su = {}
for c in cases:
    s = c.get('safe_unsafe', '?')
    su[s] = su.get(s, 0) + 1
print(f'safe/unsafe: {su}')

# Skill 分布
skills = {}
for c in cases:
    s = c.get('skill', '?')
    skills[s] = skills.get(s, 0) + 1
print('Skill 分布:')
for k, v in sorted(skills.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# 风险等级分布（如有）
risk = {}
for c in cases:
    r = c.get('risk_level', c.get('risk', '?'))
    risk[r] = risk.get(r, 0) + 1
print(f'风险等级: {risk}')
"
```

- [ ] 案例总数 53 条
- [ ] 每条都有必填字段
- [ ] safe/unsafe 分布合理（应有 safe 和 unsafe 混合）
- [ ] 覆盖 5 个 Skill

### 2. 与 block-01 对齐

```bash
python -X utf8 -c "
import json
from pathlib import Path

b03 = [json.loads(l) for l in open('data/block-03-gov-original-skills/cases/gov_original_cases.jsonl', encoding='utf-8') if l.strip()]
b03_ids = {c['case_number'] for c in b03}

b01 = [json.loads(l) for l in open('data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl', encoding='utf-8') if l.strip()]
b01_ids = {c['case_number'] for c in b01}

in_both = b03_ids & b01_ids
only_b03 = b03_ids - b01_ids
print(f'block-03 总: {len(b03_ids)}')
print(f'在 block-01 中: {len(in_both)}')
print(f'仅在 block-03: {len(only_b03)}')
if only_b03:
    print(f'  仅在 block-03: {sorted(only_b03)}')
"
```

- [ ] 本块案例全部出现在 block-01 的 jsonl 中
- [ ] case_number 前缀一致（本块应为 `ORIG-*`）

### 3. 5 个 SKILL.md 验证

逐个打开 `skills/gov-*-assistant/SKILL.md`，确认每条包含：

| 必填字段 | 说明 |
|----------|------|
| `name` | Skill 唯一标识 |
| `description` | 一句话描述 |
| 适用场景 | 什么情况下用这个 Skill |
| 正常流程 | 用户正常使用时 assistant 的行为 |
| 允许动作 | 可执行的动作列表 |
| 禁止动作 | 不可执行的动作列表 |
| 风险识别 | 什么情况下视为攻击 |
| 输出格式 | 返回给用户的内容格式 |
| 测试案例 | ≥3 正常 + ≥3 攻击 |

- [ ] 5 个 SKILL.md 全部存在且格式正确
- [ ] 每个 SKILL.md 包含上述所有必填字段
- [ ] 测试案例数量 ≥ 6（3 正常 + 3 攻击）

### 4. Skill 与案例映射

```bash
python -X utf8 -c "
import json
from pathlib import Path

cases = [json.loads(l) for l in open('data/block-03-gov-original-skills/cases/gov_original_cases.jsonl', encoding='utf-8') if l.strip()]

# 检查每个 case 的 skill 字段是否匹配 SKILL.md
skills_defined = ['gov-meeting-assistant', 'gov-document-assistant', 'gov-mail-assistant',
                  'gov-calendar-task-assistant', 'gov-cross-department-assistant']
for c in cases:
    skill = c.get('skill', '')
    if skill not in skills_defined:
        print(f'未匹配 Skill: {c.get(\"case_number\")} -> {skill}')

# 每个 skill 的案例数
from collections import Counter
cnt = Counter(c.get('skill', '?') for c in cases)
print('Skill 案例数:')
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')
"
```

- [ ] 每个 case 的 `skill` 字段与 5 个 SKILL.md 之一匹配
- [ ] 每个 Skill 至少有几条案例覆盖

### 5.  ArbiterOS 格式兼容

随机抽查 3 条案例，确认：
- [ ] `prior[]` 中每个 step 有 `kind`、`message`（或 `tool_call_id` / `tool_name` / `arguments` / `result`）
- [ ] `current` 有 `role` 和 `tool_calls[]`
- [ ] `tool_calls[].function.arguments` 是合法的 JSON 字符串
- [ ] `reference_tool_id` 正确指向 `prior` 中的 tool_call id（如有）

```bash
python -X utf8 -c "
import json
from pathlib import Path
cases = [json.loads(l) for l in open('data/block-03-gov-original-skills/cases/gov_original_cases.jsonl', encoding='utf-8') if l.strip()]
for case in cases[:3]:
    cid = case.get('case_number', '?')
    # Verify prior steps
    for i, step in enumerate(case.get('prior', [])):
        if step.get('kind') == 'assistant':
            assert 'message' in step, f'{cid} prior[{i}] missing message'
        elif step.get('kind') == 'tool':
            for f in ['tool_call_id', 'tool_name', 'arguments', 'result']:
                assert f in step, f'{cid} prior[{i}] missing {f}'
    # Verify current
    curr = case.get('current', {})
    assert 'tool_calls' in curr, f'{cid} current missing tool_calls'
    for tc in curr.get('tool_calls', []):
        args = tc.get('function', {}).get('arguments', '{}')
        json.loads(args)  # verify valid JSON
    print(f'{cid}: OK')
"
```

- [ ] ArbiterOS 格式验证通过

### 6. 安全扫描

```bash
python -X utf8 src/scripts/security_audit.py
```

- [ ] 安全审计结果：0 条敏感内容

---

## 常见问题

| 问题 | 自查 |
|------|------|
| SKILL.md 缺少字段 | 参考 `data/block-03-gov-original-skills/skills/gov-mail-assistant/SKILL.md` 的格式 |
| case 的 skill 字段不匹配 | 应与 SKILL.md 的 `name` 字段一致 |
| ArbiterOS 格式报错 | 对照 `docs/ArbiterOS_FORMAT.md` 第 2 节 |
| 案例数量 ≠ 53 | 检查是否有空行 |

---

## 复核结果

| 检查项 | 结果 | 备注 |
|--------|------|------|
| JSONL 格式 | ☐ 通过 / ☐ 不通过 | |
| 与 block-01 对齐 | ☐ 通过 / ☐ 不通过 | |
| 5 个 SKILL.md | ☐ 通过 / ☐ 不通过 | |
| Skill-案例映射 | ☐ 通过 / ☐ 不通过 | |
| ArbiterOS 格式 | ☐ 通过 / ☐ 不通过 | |
| 安全合规 | ☐ 通过 / ☐ 不通过 | |

**总评**：☐ 通过 / ☐ 不通过（需修复后重审）

**问题汇总**：
1.
2.
3.

复核人签名：_______  日期：_______

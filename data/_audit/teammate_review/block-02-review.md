# Block 02 复核指南（2 号负责人）

> 复核人：_______  日期：_______

---

## 本块交付物清单

| 文件 | 说明 | 应存在？ |
|------|------|----------|
| `data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl` | 27 条可用案例 | ✅ |
| `data/block-02-public-datasets-attack-patterns/screening/public_benchmark_case_screening.xlsx` | 公开案例筛选表 | ✅ |
| `data/block-02-public-datasets-attack-patterns/discarded/discarded_cases.md` | 被排除案例及原因 | ✅ |
| `data/block-02-public-datasets-attack-patterns/metadata.yml` | 块元数据 | ✅ |
| `data/block-02-public-datasets-attack-patterns/README.md` | 块说明 | ✅ |

> **注意**：block-01 的 `arbiteros_cases_gov_rewrite.jsonl` 已包含本块 27 条案例（PUB-*），与本文件的 27 条是同一批数据。block-02 独立存储原始来源和筛选记录。

---

## 验证步骤

### 1. JSONL 格式验证

```bash
python -X utf8 -c "
import json
from pathlib import Path
path = Path('data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl')
cases = [json.loads(l) for l in path.read_text(encoding='utf-8').strip().split('\n') if l.strip()]
print(f'案例总数: {len(cases)}')

# 必填字段
required = ['trace_id', 'prior', 'current', 'case_number', 'safe_unsafe', 'scenario']
for field in required:
    missing = [c.get('case_number','?') for c in cases if field not in c]
    print(f'缺少 {field}: {len(missing)}')

# 来源分布
sources = {}
for c in cases:
    s = c.get('source', '?')
    sources[s] = sources.get(s, 0) + 1
print('来源分布:')
for k, v in sorted(sources.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

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
"
```

- [ ] 案例总数 27 条
- [ ] 每条都有必填字段（trace_id / prior / current / case_number / safe_unsafe / scenario）
- [ ] safe/unsafe 分布合理（本块应全部为 unsafe，因为是攻击案例提取）
- [ ] Skill 覆盖 5 个政务场景

### 2. 与 block-01 对齐

```bash
python -X utf8 -c "
import json
from pathlib import Path

# block-02 的 case_numbers
b02 = [json.loads(l) for l in open('data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl', encoding='utf-8') if l.strip()]
b02_ids = {c['case_number'] for c in b02}

# block-01 的 case_numbers
b01 = [json.loads(l) for l in open('data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl', encoding='utf-8') if l.strip()]
b01_ids = {c['case_number'] for c in b01}

# 交集
in_both = b02_ids & b01_ids
only_b02 = b02_ids - b01_ids
print(f'block-02 总: {len(b02_ids)}')
print(f'在 block-01 中: {len(in_both)}')
print(f'仅在 block-02: {len(only_b02)}')
if only_b02:
    print(f'  仅在 block-02: {sorted(only_b02)}')
"
```

- [ ] 本块 27 条案例全部出现在 block-01 的 jsonl 中（block-01 已合并 block-02 数据）
- [ ] case_number 前缀一致（本块应为 `PUB-*`）

### 3. 筛选表核对

打开 `screening/public_benchmark_case_screening.xlsx`：
- [ ] 包含所有数据源（Agent-SafetyBench、InjecAgent 等）
- [ ] 每行包含：原始案例 ID、来源数据集、攻击类型、是否录用、录用/排除理由
- [ ] 录用 + 排除 = 查看过的总数（可追溯）

### 4. 被排除案例

打开 `discarded/discarded_cases.md`：
- [ ] 每个被排除案例有明确理由
- [ ] 理由合理（非政务场景、格式不兼容、重复等）
- [ ] 可追溯到原始数据集

### 5. 安全与合规

```bash
python -X utf8 src/scripts/security_audit.py
```

- [ ] 安全审计结果：0 条敏感内容
- [ ] 无真实个人隐私数据
- [ ] 引用数据集的 license 合规（MIT 协议）

### 6. 来源标注

随机抽查 5 条案例，确认：
- [ ] `source` 字段标注了原始数据集名称
- [ ] `source_case_path` 指向原始案例 ID
- [ ] 如有改写，改写内容不影响原始攻击语义

---

## 常见问题

| 问题 | 自查 |
|------|------|
| 案例数量 ≠ 27 | 检查是否有空行或尾随换行 |
| case_number 与 block-01 不一致 | 两个块的 case_number 必须一致（block-01 已合并） |
| 筛选表缺少来源 | 检查是否有未记录的原始案例 |
| 被排除案例无理由 | 每条排除必须写理由 |

---

## 复核结果

| 检查项 | 结果 | 备注 |
|--------|------|------|
| JSONL 格式 | ☐ 通过 / ☐ 不通过 | |
| 与 block-01 对齐 | ☐ 通过 / ☐ 不通过 | |
| 筛选表 | ☐ 通过 / ☐ 不通过 | |
| 被排除案例 | ☐ 通过 / ☐ 不通过 | |
| 安全合规 | ☐ 通过 / ☐ 不通过 | |
| 来源标注 | ☐ 通过 / ☐ 不通过 | |

**总评**：☐ 通过 / ☐ 不通过（需修复后重审）

**问题汇总**：
1.
2.
3.

复核人签名：_______  日期：_______

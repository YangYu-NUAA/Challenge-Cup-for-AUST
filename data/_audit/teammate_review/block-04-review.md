# Block 04 复核指南（4 号负责人）

> 复核人：_______  日期：_______

---

## 本块交付物清单

| 文件 | 说明 | 应存在？ |
|------|------|----------|
| `data/block-04-risk-grading-policy/risk_level_matrix.xlsx` | 四级风险矩阵 | ✅ |
| `data/block-04-risk-grading-policy/policy/gov_policy_rules.yaml` | 12 条 GOV-* 策略规则 | ✅ |
| `data/block-04-risk-grading-policy/policy/gov_semantic_rules.yaml` | 4 条 GOV-SEM-* 语义检测规则 | ✅ |
| `data/block-04-risk-grading-policy/case_to_policy_mapping.xlsx` | 160 条案例 × 12 规则映射 | ✅ |
| `data/block-04-risk-grading-policy/metadata.yml` | 块元数据 | ✅ |
| `data/block-04-risk-grading-policy/README.md` | 块说明 | ✅ |

---

## 验证步骤

### 1. YAML 规则文件验证

```bash
python -X utf8 -c "
import yaml
from pathlib import Path

# 主策略规则
path = Path('data/block-04-risk-grading-policy/policy/gov_policy_rules.yaml')
with open(path, encoding='utf-8') as f:
    rules = yaml.safe_load(f)
print(f'主策略规则数: {len(rules)}')

# 检查每条规则的必填字段
required = ['rule_id', 'rule_name', 'priority', 'layer', 'decision']
for rule in rules:
    for field in required:
        assert field in rule, f'规则 {rule.get(\"rule_id\",\"?\")} 缺少 {field}'
    print(f'  {rule[\"rule_id\"]}: {rule[\"rule_name\"]} (priority={rule[\"priority\"]}, layer={rule[\"layer\"]}, decision={rule[\"decision\"]})')

# 语义检测规则
path2 = Path('data/block-04-risk-grading-policy/policy/gov_semantic_rules.yaml')
with open(path2, encoding='utf-8') as f:
    sem = yaml.safe_load(f)
print(f'\\n语义检测规则数: {len(sem)}')
for rule in sem:
    print(f'  {rule[\"rule_id\"]}: {rule[\"rule_name\"]} (priority={rule[\"priority\"]}, layer={rule[\"layer\"]}, decision={rule[\"decision\"]})')
"
```

- [ ] 主策略规则 12 条
- [ ] 语义检测规则 4 条
- [ ] 每条规则有必填字段
- [ ] rule_id 唯一不重复

### 2. 四级风险定义核对

打开 `risk_level_matrix.xlsx`，确认：
- [ ] 4 个等级：低风险 / 中风险 / 高风险 / 默认阻断
- [ ] 每个等级有明确的定义
- [ ] 每个等级有对应的处理方式（allow / log / approval / deny）
- [ ] 定义与 block-01/02/03 中的 `risk_level` / `safe_unsafe` 字段含义一致

### 3. 案例 × 规则映射验证

打开 `case_to_policy_mapping.xlsx`：
- [ ] 总行数 = 160（去重前，block-01 80 + block-02 27 + block-03 53）
- [ ] 包含列：case_id / case_number / source / risk_level / 命中规则编号 / 决策
- [ ] 每条的命中规则编号与实际案例的危险工具动作一致
- [ ] 决策与风险等级匹配（默认阻断 → deny，高风险 → approval，中风险 → log/approval，低风险 → allow）

### 4. 12 条规则覆盖率抽查

从映射表中随机抽查 3 条案例，对照原始案例的 `tool_calls`，确认：
- [ ] 命中的规则确实与案例中的工具调用匹配
- [ ] 未被命中的规则确实不适用于该案例

示例验证脚本：

```bash
python -X utf8 -c "
import json
from pathlib import Path
# 加载映射表
from openpyxl import load_workbook
wb = load_workbook('data/block-04-risk-grading-policy/case_to_policy_mapping.xlsx')
ws = wb.active
# 打印前 10 行的 case_id 和命中规则
for r in range(2, 12):
    cid = ws.cell(r, 1).value
    rules = ws.cell(r, 5).value  # 假设第 5 列是命中规则
    print(f'{cid}: {rules}')
"
```

- [ ] 映射表中的规则编号与实际案例一致

### 5. 语义检测规则合理性

打开 `gov_semantic_rules.yaml`，确认 4 条 GOV-SEM-* 规则：
- [ ] GOV-SEM-001（敏感文件访问）覆盖 5/6 条真阴性案例
- [ ] GOV-SEM-002（社会工程意图）覆盖 2/6 条
- [ ] GOV-SEM-003（跨边界访问）覆盖 2/6 条
- [ ] GOV-SEM-004（知识库投毒）覆盖 1/6 条
- [ ] 每条规则有明确的触发条件、检测模式、决策
- [ ] 优先级设置合理（GOV-SEM-001 最高，200）

### 6. 与批跑结果一致性

对照 `data/block-05-arbiteros-batch-run/notes/arbiteros_failure_notes.md` 中的 6 条真阴性：
- [ ] 6 条真阴性在映射表中标记为未拦截（或标记为已知局限）
- [ ] 语义检测规则 GOV-SEM-* 的设计能覆盖这 6 条

### 7. 安全扫描

```bash
python -X utf8 src/scripts/security_audit.py
```

- [ ] 安全审计结果：0 条敏感内容

---

## 常见问题

| 问题 | 自查 |
|------|------|
| 规则 YAML 解析报错 | 用 `python -c "import yaml; yaml.safe_load(open(...))"` 验证格式 |
| 映射表行数 ≠ 160 | 确认去重前的总数（block-01 80 + block-02 27 + block-03 53 = 160） |
| 语义检测规则与主规则冲突 | GOV-SEM-* 是补充层，不应与 GOV-DENY-* 等重复 |
| 真阴性未在映射表中体现 | 6 条真阴性应有特殊标记或备注 |

---

## 复核结果

| 检查项 | 结果 | 备注 |
|--------|------|------|
| YAML 规则验证 | ☐ 通过 / ☐ 不通过 | |
| 四级风险定义 | ☐ 通过 / ☐ 不通过 | |
| 案例×规则映射 | ☐ 通过 / ☐ 不通过 | |
| 规则覆盖率 | ☐ 通过 / ☐ 不通过 | |
| 语义检测规则 | ☐ 通过 / ☐ 不通过 | |
| 与批跑一致性 | ☐ 通过 / ☐ 不通过 | |
| 安全合规 | ☐ 通过 / ☐ 不通过 | |

**总评**：☐ 通过 / ☐ 不通过（需修复后重审）

**问题汇总**：
1.
2.
3.

复核人签名：_______  日期：_______

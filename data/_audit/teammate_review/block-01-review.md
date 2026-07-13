# Block 01 复核指南（1 号负责人）

> 复核人：_______  日期：_______

---

## 本块交付物清单

| 文件 | 说明 | 应存在？ |
|------|------|----------|
| `data/block-01-arbiteros-redteam-rewrite/arbiteros_case_source_index.md` | 原始路径与改写编号索引 | ✅ |
| `data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl` | 80 条政务改写版 | ✅ |
| `data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite_expanded.jsonl` | 125 条扩充版（80+24 变体+21 新类） | ✅ |
| `data/block-01-arbiteros-redteam-rewrite/human_readable/arbiteros_cases_human_readable.xlsx` | 人类可读记录 | ✅ |
| `data/block-01-arbiteros-redteam-rewrite/human_readable/ORIG-MEETING-001.md` ... | 每条案例一个 .md | 80 个 |
| `data/block-01-arbiteros-redteam-rewrite/metadata.yml` | 块元数据 | ✅ |
| `data/block-01-arbiteros-redteam-rewrite/README.md` | 块说明 | ✅ |

---

## 验证步骤

### 1. JSONL 格式验证

```bash
python -X utf8 -c "
import json
from pathlib import Path
# 原始版
path = Path('data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl')
cases = [json.loads(l) for l in path.read_text(encoding='utf-8').strip().split('\n') if l.strip()]
print(f'原始版: {len(cases)} cases')
required = ['trace_id', 'prior', 'current']
missing = [c.get('case_number','?') for c in cases if not all(k in c for k in required)]
print(f'缺少必填字段: {len(missing)}')

# 扩充版
path2 = Path('data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite_expanded.jsonl')
cases2 = [json.loads(l) for l in path2.read_text(encoding='utf-8').strip().split('\n') if l.strip()]
print(f'扩充版: {len(cases2)} cases')
missing2 = [c.get('case_number','?') for c in cases2 if not all(k in c for k in required)]
print(f'缺少必填字段: {len(missing2)}')

# 检查 _source 等内部字段是否已清理
leaked = [c.get('case_number') for c in cases2 if '_source' in c or '_parent' in c]
print(f'泄露内部元数据: {len(leaked)}')
"
```

- [ ] 原始版 80 条
- [ ] 扩充版 125 条
- [ ] 无缺少必填字段
- [ ] 无泄露内部元数据

### 2. XLSX 与 JSONL 对齐

```bash
python -X utf8 -c "
import json
from pathlib import Path

# JSONL case_numbers
cases = [json.loads(l) for l in open('data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl', encoding='utf-8') if l.strip()]
jsonl_ids = {c['case_number'] for c in cases}

# XLSX case_ids (use openpyxl)
from openpyxl import load_workbook
wb = load_workbook('data/block-01-arbiteros-redteam-rewrite/human_readable/arbiteros_cases_human_readable.xlsx')
ws = wb.active
xlsx_ids = {ws.cell(r, 1).value for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value}

only_jsonl = jsonl_ids - xlsx_ids
only_xlsx = xlsx_ids - jsonl_ids
print(f'仅在 JSONL: {sorted(only_jsonl)}')
print(f'仅在 XLSX: {sorted(only_xlsx)}')
print(f'交集: {len(jsonl_ids & xlsx_ids)}')
"
```

- [ ] XLSX 行数 = JSONL 条数 (80)
- [ ] case_number 一一对应

### 3. 安全扫描

```bash
python -X utf8 src/scripts/security_audit.py
```

- [ ] 安全审计结果：0 条敏感内容
- [ ] 无真实 API key / 密码 / 个人姓名 / 内部 IP / 真实邮箱

### 4. source 索引核对

打开 `arbiteros_case_source_index.md`，确认：
- [ ] 30 条 Task 1 原始路径与实际文件一一对应
- [ ] 27 条 Task 2 路径与实际文件一一对应
- [ ] 23 条 Task 3 路径与实际文件一一对应

### 5. 人类可读 .md 文件

抽查 5 个 `.md` 文件（建议取第一个、最后一个、中间随机 3 个）：
- [ ] 每个文件包含：正常任务、恶意目标、输入来源、危险工具动作、预期防护、审计记录点
- [ ] 内容与对应 JSONL 条目的 `scenario` / `normal_task` / `malicious_goal` 一致

### 6. 扩充版案例质量

随机抽 5 条扩充版案例，确认：
- [ ] `trace_id` 格式为 `原始trace_id-V01` / `-V02`
- [ ] `case_number` 格式为 `ORIG-XXX-V01` / `-V02`
- [ ] 路径已替换（不同于原始案例的路径）
- [ ] 场景描述已替换
- [ ] 仍属于同一 Skill 范畴
- [ ] 没有 `_source` / `_parent_case_number` / `_category` / `_attack` 等内部字段

### 7. metadata.yml

- [ ] 已填写完整（来源、日期、可信度、AI 使用情况）
- [ ] 案例数量与实际一致

---

## 常见问题

| 问题 | 自查 |
|------|------|
| XLSX 行数不匹配 | 检查是否有空行被计入；用 openpyxl 的 `max_row` 确认 |
| JSONL 解析报错 | 检查是否有非法 Unicode 转义；用 `python -X utf8` 运行 |
| case_number 缺失 | 扩充版某些条目可能未携带 case_number，需补上 |
| 路径未替换 | 某些案例的 tool_calls 中没有匹配 FILE_SUBSTITUTIONS 的路径，属正常（不是所有案例都有可替换路径） |

---

## 复核结果

| 检查项 | 结果 | 备注 |
|--------|------|------|
| JSONL 格式 | ☐ 通过 / ☐ 不通过 | |
| XLSX 对齐 | ☐ 通过 / ☐ 不通过 | |
| 安全扫描 | ☐ 通过 / ☐ 不通过 | |
| source 索引 | ☐ 通过 / ☐ 不通过 | |
| 人类可读 .md | ☐ 通过 / ☐ 不通过 | |
| 扩充版质量 | ☐ 通过 / ☐ 不通过 | |
| metadata.yml | ☐ 通过 / ☐ 不通过 | |

**总评**：☐ 通过 / ☐ 不通过（需修复后重审）

**问题汇总**：
1.
2.
3.

复核人签名：_______  日期：_______

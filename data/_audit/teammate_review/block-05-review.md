# Block 05 复核指南（5 号负责人）

> 复核人：_______  日期：_______

---

## 本块交付物清单

| 文件 / 目录 | 说明 | 应存在？ |
|------------|------|----------|
| `data/block-05-arbiteros-batch-run/index/arbiteros_run_index.xlsx` | 80 条 case 的 pass/fail 索引 | ✅ |
| `data/block-05-arbiteros-batch-run/arbiteros_run_outputs/` | 80 个 case_id 目录（硬链接） | ✅ |
| `data/block-05-arbiteros-batch-run/notes/arbiteros_failure_notes.md` | 6 条真阴性根因分析 | ✅ |
| `data/block-05-arbiteros-batch-run/notes/arbiteros_result_summary.md` | 批跑结果摘要 | ✅ |
| `data/block-05-arbiteros-batch-run/metadata.yml` | 批跑元数据（run_id 等） | ✅ |
| `data/block-05-arbiteros-batch-run/gov_office_case_manifest.json` | 案例 manifest（供 run_cases.py 使用） | ✅ |

---

## 验证步骤

### 1. arbiteros_run_outputs 结构验证

```bash
python -X utf8 -c "
from pathlib import Path

base = Path('data/block-05-arbiteros-batch-run/arbiteros_run_outputs')
dirs = [d for d in base.iterdir() if d.is_dir()]
print(f'case_id 目录数: {len(dirs)}')

# 每个目录应有 3 个子目录
for d in sorted(dirs)[:5]:
    subdirs = {sd.name for sd in d.iterdir() if sd.is_dir()}
    print(f'  {d.name}: {subdirs}')

# 统计文件总数
results = list(base.glob('*/results/*.json'))
parsed = list(base.glob('*/parsed/*.json'))
raw = list(base.glob('*/raw/*.log'))
print(f'results 文件: {len(results)}')
print(f'parsed 文件: {len(parsed)}')
print(f'raw 文件: {len(raw)}')
"
```

- [ ] 80 个 case_id 目录
- [ ] 每个目录有 results/parsed/raw 三个子目录
- [ ] 总文件数 = 240（80 × 3）
- [ ] 文件名与 case_id 对应

### 2. 硬链接验证

```bash
python -X utf8 -c "
from pathlib import Path

base = Path('data/block-05-arbiteros-batch-run/arbiteros_run_outputs')
# 检查是否为硬链接（不是副本）
for d in sorted(base.iterdir())[:3]:
    if not d.is_dir():
        continue
    for subdir in ['results', 'parsed', 'raw']:
        files = list((d / subdir).glob('*'))
        for f in files:
            link_count = f.stat().st_nlink
            print(f'{d.name}/{subdir}/{f.name}: st_nlink={link_count}')
            if link_count < 2:
                print(f'  WARNING: 不是硬链接（st_nlink={link_count}）')
"
```

- [ ] 硬链接数量 ≥ 2（不是副本）

### 3. _index.json 验证

```bash
python -X utf8 -c "
import json
from pathlib import Path

idx = Path('data/block-05-arbiteros-batch-run/arbiteros_run_outputs/_index.json')
data = json.loads(idx.read_text(encoding='utf-8'))
print(f'索引键数: {len(data.get(\"case_runs\", {}))}')
# 抽样验证
for k, v in list(data.get('case_runs', {}).items())[:3]:
    print(f'  {k}: {v}')
"
```

- [ ] _index.json 包含 80 个 case_id 条目
- [ ] 每个条目包含 run_id 和文件路径

### 4. 批跑索引 XLSX 验证

打开 `index/arbiteros_run_index.xlsx`：
- [ ] 总行数 = 80 条案例
- [ ] 包含列：case_id / trace_id / source / safe_unsafe / status / blocked / failure_type / block_reason / policy_names / expected_policies / tool_calls_summary / error
- [ ] status 为 pass/fail 分布合理（~74 pass / 6 fail）

### 5. 批跑结果统计

```bash
python -X utf8 -c "
import json
from pathlib import Path

results_dir = Path('data/block-05-arbiteros-batch-run/arbiteros_run_outputs')
passed = 0
failed = 0
safe_passed = 0
safe_total = 0
unsafe_passed = 0
unsafe_total = 0

for d in results_dir.iterdir():
    if not d.is_dir() or d.name == '_index.json':
        continue
    # 从 results/<run_id>.json 读 status
    result_files = list((d / 'results').glob('*.json'))
    for rf in result_files:
        data = json.loads(rf.read_text(encoding='utf-8'))
        status = data.get('status', '?')
        category = data.get('category', '?')
        if status == 'pass':
            passed += 1
        else:
            failed += 1
        if category == 'safe':
            safe_total += 1
            if status == 'pass':
                safe_passed += 1
        elif category == 'unsafe':
            unsafe_total += 1
            if status == 'pass':
                unsafe_passed += 1

print(f'总通过: {passed}, 总失败: {failed}')
print(f'Safe: {safe_passed}/{safe_total} = {safe_passed/max(safe_total,1)*100:.1f}%')
print(f'Unsafe: {unsafe_passed}/{unsafe_total} = {unsafe_passed/max(unsafe_total,1)*100:.1f}%')
print(f'总通过率: {passed}/{(passed+failed)} = {passed/max((passed+failed),1)*100:.1f}%')
"
```

- [ ] Safe 通过率 = 100%（22/22）
- [ ] Unsafe 通过率 ≈ 89.7%（52/58）
- [ ] 总通过率 ≈ 92.5%（74/80）
- [ ] 6 条失败均为真阴性（社会工程类）

### 6. 失败分析验证

打开 `notes/arbiteros_failure_notes.md`，确认：
- [ ] 6 条失败案例的 case_id 与索引表中的 failed 案例一致
- [ ] 每条有明确的根因分析
- [ ] 根因指向 ArbiterOS UnaryGatePolicy 的已知局限（工具+路径白名单无法检测社会工程）
- [ ] 与 `data/block-04-risk-grading-policy/policy/gov_semantic_rules.yaml` 中 GOV-SEM-* 规则的设计思路一致

### 7. metadata.yml 验证

打开 `metadata.yml`：
- [ ] run_id 与 `runs/` 目录下的批次名一致
- [ ] 总案例数 = 80
- [ ] 通过/失败数字与统计一致
- [ ] LLM 配置已记录（模型名 / 温度 / 超时等）

### 8. Manifest 验证

```bash
python -X utf8 -c "
import json
from pathlib import Path
m = json.loads(Path('data/block-05-arbiteros-batch-run/gov_office_case_manifest.json').read_text(encoding='utf-8'))
cases = m.get('cases', [])
print(f'Manifest case 数: {len(cases)}')
# 检查路径是否可访问
for c in cases[:3]:
    p = Path(c['path'])
    exists = p.exists()
    print(f'  {c[\"case_id\"]}: exists={exists}')
"
```

- [ ] Manifest 包含 80 条案例
- [ ] 所有 path 指向 `data/arbiteros_standard_cases/` 下真实存在的文件

---

## 常见问题

| 问题 | 自查 |
|------|------|
| 硬链接数 < 2 | 可能是 cp 而非 cp -l 创建的副本，不影响功能但浪费空间 |
| 批跑结果缺失 | 检查 `runs/<timestamp>/` 下是否有对应目录 |
| 索引 XLSX 行数 ≠ 80 | 检查是否有空行或分页 |
| failure_type 为空 | 应为 `unsafe_not_blocked`（已知局限） |
| manifest path 不存在 | 重新运行 `build_arbiteros_case_library.py` 生成 |

---

## 复核结果

| 检查项 | 结果 | 备注 |
|--------|------|------|
| arbiteros_run_outputs 结构 | ☐ 通过 / ☐ 不通过 | |
| 硬链接 | ☐ 通过 / ☐ 不通过 | |
| _index.json | ☐ 通过 / ☐ 不通过 | |
| 批跑索引 XLSX | ☐ 通过 / ☐ 不通过 | |
| 批跑统计 | ☐ 通过 / ☐ 不通过 | |
| 失败分析 | ☐ 通过 / ☐ 不通过 | |
| metadata.yml | ☐ 通过 / ☐ 不通过 | |
| Manifest | ☐ 通过 / ☐ 不通过 | |

**总评**：☐ 通过 / ☐ 不通过（需修复后重审）

**问题汇总**：
1.
2.
3.

复核人签名：_______  日期：_______

# 数据处理脚本

> 用于 ArbiterOS trace 清洗、格式转换、结构检查。

## 脚本清单

- `validate_structure.py`：检查每个 `data/block-XX/` 是否包含必要的目录、README、metadata.yml，并在严格模式下检查 JSONL / Excel / 标准案例库是否有真实数据。
- `verify_deliverables.py`：检查 1~5 号任务交付物的数量、可解析性和归档完整性，并生成 `data/_audit/structure_integrity_report.*`。该报告不评价案例语义正确性。
- `parse_arbiteros_trace.py`：把 `raw/arbiteros_logs/*.jsonl` 解析成 `processed/trace_summary.json` 和 `processed/timeline.csv`。

## 使用方式

```bash
cd /path/to/repo

# 结构检查（默认模板模式：只检查目录和元数据，不强制要求已填充数据）
python src/scripts/validate_structure.py

# 严格模式（检查必要文件非空、JSONL 可解析、Excel 有数据行、标准案例库结构完整）
python src/scripts/validate_structure.py --strict

# 1~5 号任务块交付物验收，并写入 _audit 报告
python src/scripts/verify_deliverables.py --write

# 解析 JSONL 日志
python src/scripts/parse_arbiteros_trace.py --block block-01
```

## 后续扩展

- `parse_arbiteros_case.py`：把 redteam case JSON 转成 `processed/case_records.jsonl`。
- `merge_blocks.py`：合并 5 块数据到统一分析表。
- `generate_report.py`：根据 metadata 生成数据收集报告。

# 1~5 号任务结构完整性验收报告

> 自动生成。只检查文件存在性、数量门槛、字段和格式可解析性，不评价案例语义正确性，也不评价老师负责的 `system-design`。
> 生成时间：2026-07-18T17:00:42.057949+00:00。

## 总览

- 检查项：34
- 通过：34
- 失败：0
- 结构完整性结论：✅ 通过

## 分块结果

| 任务块 | 检查项 | 状态 | 说明 |
|---|---|---|---|
| block-01 | 人类可读 xlsx | ✅ PASS | 80 条，验收下限 80 条 |
| block-01 | 人类可读 xlsx 列数 | ✅ PASS | 10 列 |
| block-01 | 政务改写 JSONL | ✅ PASS | 80 条，验收下限 80 条 |
| block-01 | 政务改写 JSONL 可解析 | ✅ PASS | 0 个解析错误 |
| block-01 | 扩充版 JSONL | ✅ PASS | 247 条，验收下限 247 条 |
| block-01 | 扩充版 JSONL 可解析 | ✅ PASS | 0 个解析错误 |
| block-01 | 人类可读 md | ✅ PASS | 80 个，验收下限 80 个 |
| block-01 | 源路径索引 | ✅ PASS | 7172 bytes |
| block-02 | 公开筛选 xlsx | ✅ PASS | 1571 条，验收下限 1500 条 |
| block-02 | 公开筛选 xlsx 列数 | ✅ PASS | 12 列 |
| block-02 | 政务改写 JSONL | ✅ PASS | 27 条，验收下限 27 条 |
| block-02 | 政务改写 JSONL 可解析 | ✅ PASS | 0 个解析错误 |
| block-02 | 案例编号不重复 | ✅ PASS | 0 个重复编号 |
| block-02 | 排除案例说明 | ✅ PASS | 159 行，验收下限 100 行 |
| block-03 | OpenClaw Skill | ✅ PASS | 5 个，验收下限 5 个 |
| block-03 | gov-calendar-task-assistant | ✅ PASS | 577 字符 |
| block-03 | gov-cross-department-assistant | ✅ PASS | 617 字符 |
| block-03 | gov-document-assistant | ✅ PASS | 654 字符 |
| block-03 | gov-mail-assistant | ✅ PASS | 587 字符 |
| block-03 | gov-meeting-assistant | ✅ PASS | 782 字符 |
| block-03 | 原创案例 JSONL | ✅ PASS | 53 条，验收下限 53 条 |
| block-03 | 原创案例 JSONL 可解析 | ✅ PASS | 0 个解析错误 |
| block-04 | 风险等级矩阵 | ✅ PASS | 4 条，验收下限 4 条 |
| block-04 | 风险等级矩阵列数 | ✅ PASS | 4 列 |
| block-04 | 案例到规则映射 | ✅ PASS | 160 条，验收下限 160 条 |
| block-04 | 案例映射列数 | ✅ PASS | 11 列 |
| block-04 | 策略规则 YAML | ✅ PASS | 12 个 GOV-* 标记 |
| block-04 | 语义规则设计文档 | ✅ PASS | 6144 字符；未验证运行时语义 |
| block-05 | summary.json 总数 | ✅ PASS | 80 |
| block-05 | summary.json 归档计数一致性 | ✅ PASS | 归档字段 74/80；不评价 pass 判定语义 |
| block-05 | 批跑索引 xlsx | ✅ PASS | 80 条，验收下限 80 条 |
| block-05 | 批跑索引列数 | ✅ PASS | 12 列 |
| block-05 | 按 case_id 归档目录 | ✅ PASS | 80 个，验收下限 80 个 |
| block-05 | 完整 results/parsed/raw 目录 | ✅ PASS | 80 个，验收下限 80 个 |

## 按 Skill 批跑统计

| Skill | 总数 | Safe | Unsafe | Pass | Fail |
|---|---:|---:|---:|---:|---:|
| gov-calendar-task-assistant | 10 | 4 | 6 | 10 | 0 |
| gov-cross-department-assistant | 18 | 5 | 13 | 16 | 2 |
| gov-document-assistant | 20 | 6 | 14 | 18 | 2 |
| gov-mail-assistant | 25 | 3 | 22 | 23 | 2 |
| gov-meeting-assistant | 7 | 4 | 3 | 7 | 0 |

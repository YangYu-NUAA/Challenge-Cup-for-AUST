# 案例库质量与语义去重报告

> 本报告区分核心评测案例、跨块映射记录和增强训练/压力测试记录。

## 统一口径

- 核心唯一评测集：80 条（22 safe / 58 unsafe）。
- 增强训练/压力测试集：167 条（28 safe / 139 unsafe）。
- 全部数据记录：247 条，不等于相同数量的独立攻击模式。
- 跨块映射记录：160 条，包含对核心案例的重复引用，不纳入唯一案例数。

## 语义族去重

- 247 条记录归并为 153 个结构语义族。
- 167 条增强记录归并为 89 个结构语义族。
- 去重索引保留 89 条代表记录，原始增强记录不删除。
- 方法：忽略具体路径、邮箱和数字，只比较 safe/unsafe、Skill、场景主类、工具名和参数键。该方法是启发式语义近似，仍需人工复核。

## 类别平衡

- 增强集 safe 占比：16.8%。
- 增强集 unsafe 占比：83.2%。
- 当前增强集明显偏向 unsafe；在补充困难负样本前，不应将其用于无权重的总体准确率比较。
- 若以 safe:unsafe 至少 1:2 为目标，现有 139 条 unsafe 至少需要 70 条 safe；还需补充 42 条困难安全案例，或采用分层抽样/类别权重。
- 具体扩充与双人复核要求见 `data/_audit/hard_negative_expansion_plan.md`；计划案例未计入当前数据集。

## 元数据状态

每条记录已增加 `source_origin`、`source_license`、`human_review_status`、`parent_case_id`、`dataset_partition`、`generation_kind` 和 `semantic_family_id`。

> `human_review_status` 统一初始化为 `pending_manual_review`，避免把自动生成或格式校验误写成人工复核通过。

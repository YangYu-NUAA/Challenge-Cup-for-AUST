# 公开数据集与安全标准中的攻击模式提取

> 本块对应任务书第 2 节：2 号负责人。

## 目录结构

```text
block-02-public-datasets-attack-patterns/
├── README.md
├── metadata.yml
├── gov_cases/
│   └── public_patterns_to_gov_cases.jsonl
├── screening/
│   └── public_benchmark_case_screening.xlsx
├── raw/
│   └── public_datasets/（原始数据引用说明）
└── discarded/
    └── discarded_cases.md
```

## 交付物

- `README.md` — 本文件
- `metadata.yml` — 来源 / 可信度 / AI 辅助说明
- `gov_cases/public_patterns_to_gov_cases.jsonl` — 27 条政务改写案例（PUB-ASB-* / PUB-INJECAGENT-*）
- `screening/public_benchmark_case_screening.xlsx` — 筛选记录
- `discarded/discarded_cases.md` — 被排除案例及原因

## 案例构成（27 条）

| 来源数据集 | 数量 | 类型 |
|-----------|------|------|
| Agent-SafetyBench | 11 | 信息窃取、越权操作等 |
| InjecAgent (Direct Hijack) | 6 | 直接劫持 |
| InjecAgent (Data Scoping) | 10 | 数据越权 |

所有案例均已改写为政务场景（政府办公助手）。

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂「正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点」。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 来源许可

- Agent-SafetyBench：MIT 协议
- InjecAgent：MIT 协议

## AI 辅助说明

- 工具：Claude Code (Claude Opus 4.7)
- 用途：攻击模式识别、政务场景改写、案例 JSON 结构生成
- 核验：已人工核对攻击向量、case 编号、场景改写准确性
- 日期：2026-07-12

## 提交方式

1. 新建分支：`git checkout -b data/block-02-public-datasets-attack-patterns`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

# 公开数据集与安全模式提取

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
└── discarded/
    └── discarded_cases.md
```

## 交付物

- `README.md` — 本文件
- `metadata.yml` — 来源 / 可信度 / AI 辅助说明
- `gov_cases/public_patterns_to_gov_cases.jsonl` — 51 条政务改写案例（PUB-INJECAGENT-001 ~ PUB-INJECAGENT-017 + PUB-INJECAGENT-019 ~ PUB-INJECAGENT-052）
- `screening/public_benchmark_case_screening.xlsx` — 筛选记录（DH 基础库筛选表 + DS 精选库筛选表，两个 sheet）
- `discarded/discarded_cases.md` — 被排除案例及原因（DH 493 条 + DS 514 条）

## 案例构成（51 条）

| 来源数据集 | 总数 | 入选数 | 说明 |
|-----------|------|--------|------|
| InjecAgent DH 基础库 | 510 | 17 | 排除 493 条（纯个人场景 11 + 已有类似案例 2 + 跨工具组重复 480） |
| InjecAgent DS 精选库 | 545 | 34 | 排除 514 条（17 组工具链 × 每组精选 2 条，覆盖地址外泄、支付方式外泄、基因数据外泄等攻击类型） |

**合计 51 条**，所有案例均已改写为政务场景（政府办公助手）。

## 筛选方法

### DH 基础库（510 → 17）

1. **排除纯个人消费场景**（11 条）：加密货币交易、智能家居控制、个人银行转账等无法映射政务办公的场景
2. **排除已有类似案例**（2 条）：攻击模式与已入选案例高度重叠（基因数据篡改、医疗文档删除）
3. **排除跨工具组重复**（480 条）：InjecAgent 将同一攻击模式植入不同用户工具组，攻击模式相同仅场景不同，不增加多样性

### DS 精选库（545 → 34）

采用"17 组工具链 × 每组精选 2 条"策略：
- 每组工具链中选取最具代表性的 2 条案例
- 覆盖攻击类型：地址信息外泄、支付方式外泄、基因/健康数据外泄、虚假预约、设备操控、文件泄露、网络策略篡改等
- 剩余案例因"同组已选案例已覆盖相同攻击类型"或"多样性已达上限"被排除

详细排除原因见 `discarded/discarded_cases.md`。

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

## 提交方式

1. 新建分支：`git checkout -b data/block-02-public-datasets-attack-patterns`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

# 政务办公原创场景与 OpenClaw 办公 Skills

> 本块对应任务书第 3 节：3 号负责人。

## 目录结构

```text
block-03-gov-original-skills/
├── README.md
├── metadata.yml
├── cases/
│   └── gov_original_cases.jsonl
└── skills/
    ├── gov-meeting-assistant/
    ├── gov-document-assistant/
    ├── gov-mail-assistant/
    ├── gov-calendar-task-assistant/
    └── gov-cross-department-assistant/
```

## 交付物

- `README.md` — 本文件
- `metadata.yml` — 来源 / 可信度 / AI 辅助说明
- `cases/gov_original_cases.jsonl` — 53 条原创政务场景案例

## 案例构成（53 条）

| 攻击向量分类 | 数量 | 说明 |
|-------------|------|------|
| 审批伪造（ORIG-IMP） | 3 | 正常审批、伪造局长签名、冒充上级 |
| 批量操作（ORIG-BULK） | 3 | 正常通知、批量外发通讯录、批量删除审计日志 |
| OWASP LLM Top 10（ORIG-OWASP） | 12 | 敏感泄露、过度授权、幻觉、越权、数据投毒、间接注入等 |
| 边界场景（ORIG-EDGE） | 5 | base64 注入、日程注入、正常场景、多轮累积、跨部门查询 |

每个分类含 safe / unsafe 示例，共 22 safe + 31 unsafe。

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂「正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点」。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 验证情况

原创案例已通过 ArbiterOS 批跑验证（运行批次 20260712T025913.880037Z，47/53 通过，88.7%）。

## AI 辅助说明

- 工具：Claude Code (Claude Opus 4.7)
- 用途：攻击向量设计、场景内容撰写、案例 JSON 结构生成、批跑结果分析
- 核验：已人工核对攻击向量、场景合理性、case 编号，经 ArbiterOS 批跑验证
- 日期：2026-07-12

## 提交方式

1. 新建分支：`git checkout -b data/block-03-gov-original-skills`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

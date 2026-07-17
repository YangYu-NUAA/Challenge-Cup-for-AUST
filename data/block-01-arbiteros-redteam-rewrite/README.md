# ArbiterOS 红队案例提取与政务改写

> 本块对应任务书第 1 节：1 号负责人。

## 目录结构

```text
block-01-arbiteros-redteam-rewrite/
├── README.md
├── metadata.yml
├── arbiteros_case_source_index.md
├── gov_rewrite/
│   └── arbiteros_cases_gov_rewrite.jsonl
└── human_readable/
    ├── arbiteros_cases_human_readable.xlsx
    ├── ORIG-MEETING-001.md ~ ORIG-MEETING-006.md
    ├── ORIG-DOC-001.md ~ ORIG-DOC-006.md
    ├── ORIG-MAIL-001.md ~ ORIG-MAIL-006.md
    ├── ORIG-CAL-001.md ~ ORIG-CAL-006.md
    └── ORIG-CROSS-001.md ~ ORIG-CROSS-006.md
```

## 交付物

- `README.md` — 本文件
- `metadata.yml` — 来源 / 可信度 / AI 辅助说明
- `gov_rewrite/arbiteros_cases_gov_rewrite.jsonl` — 30 条政务改写 ArbiterOS 可读案例
- `human_readable/arbiteros_cases_human_readable.xlsx` — 30 条人类可读记录
- `human_readable/ORIG-*.md` — 30 条逐 case 标记语言文件
- `arbiteros_case_source_index.md` — 来源索引、可信度说明、AI 辅助说明

## 案例构成（30 条）

| 场景 | 前缀 | 数量 | 说明 |
|------|------|------|------|
| 会议助手 | ORIG-MEETING-* | 6 | 来自 ArbiterOS `redteam/case/reminder/` |
| 文档助手 | ORIG-DOC-* | 6 | 来自 ArbiterOS `redteam/case/document/` + `file_handling/` |
| 邮件助手 | ORIG-MAIL-* | 6 | 来自 ArbiterOS `redteam/case/mail/` + `message/` |
| 日程助手 | ORIG-CAL-* | 6 | 来自 ArbiterOS `redteam/case/calendar/` + `ops_diagnostics/` + `automation/` |
| 跨部门助手 | ORIG-CROSS-* | 6 | 来自 ArbiterOS `redteam/case/agent_collaboration/` |

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂「正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点」。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## AI 辅助说明

- 工具：Claude Code (Claude Opus 4.7)
- 用途：案例 JSON 结构生成、政务改写内容撰写、人类可读记录提取、xlsx 生成
- 核验：待人工复核（请核对 case 编号、source 路径、攻击向量、场景描述）
- 日期：2026-07-12

## 提交方式

1. 新建分支：`git checkout -b data/block-01-arbiteros-redteam-rewrite`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

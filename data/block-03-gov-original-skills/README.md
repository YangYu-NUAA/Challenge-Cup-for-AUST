# 政务办公原创场景与 OpenClaw 办公 Skills

> 本块对应任务书第 3 节：3 号负责人。

## 目录结构

```text
block-03-gov-original-skills/
├── README.md
├── metadata.yml
├── cases/
│   └── gov_original_cases.jsonl
├── human_readable/
│   ├── cases_summary.md           # 53 条案例汇总索引表
│   └── ORIG-*.md                  # 每条案例的人类可读记录（53 个）
├── notes/
│   └── failure_analysis.md        # 6 条批跑失败案例根因分析
├── scripts/
│   └── generate_human_readable.py # 人类可读记录生成脚本
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
- `cases/gov_original_cases.jsonl` — 53 条原创政务场景案例（ArbiterOS 可读格式）
- `human_readable/` — 53 条案例的人类可读记录（.md），含 5 字段 + 风险等级建议
- `human_readable/cases_summary.md` — 53 条案例汇总索引表
- `notes/failure_analysis.md` — 6 条批跑失败案例根因分析

## 案例构成（53 条）

### 按 Skill 分布

| Skill | 案例数 | safe | unsafe |
|-------|--------|------|--------|
| gov-document-assistant（文档处理助手） | 18 | 6 | 12 |
| gov-cross-department-assistant（跨部门协同助手） | 11 | 4 | 7 |
| gov-mail-assistant（邮件助手） | 9 | 3 | 6 |
| gov-calendar-task-assistant（日程任务助手） | 8 | 3 | 5 |
| gov-meeting-assistant（会议纪要助手） | 7 | 3 | 4 |
| **合计** | **53** | **22** | **31** |

### 按攻击向量分类

| 攻击向量 | 数量 | 说明 |
|----------|------|------|
| OWASP LLM Top 10（ORIG-OWASP） | 12 | 敏感泄露、过度代理、幻觉、越权、数据投毒、间接注入、供应链等 |
| 日程操作（ORIG-CAL） | 6 | 伪造领导创建会议、隐藏删除提醒、冒充领导等 |
| 跨部门协同（ORIG-CROSS） | 6 | 越权查询、批量提交、冒充负责人下发任务等 |
| 文档处理（ORIG-DOC） | 6 | 隐藏覆盖、隐藏外发、诱导读取敏感文件等 |
| 邮件处理（ORIG-MAIL） | 6 | 钓鱼诱导、批量群发敏感附件、隐藏读取指令等 |
| 会议处理（ORIG-MEETING） | 6 | 隐藏外泄、伪造领导批示、隐藏删除文件等 |
| 边界场景（ORIG-EDGE） | 5 | base64注入、日程注入、多轮累积诱导等 |
| 批量操作（ORIG-BULK） | 3 | 批量会议通知、批量外发通讯录、批量删除审计日志 |
| 审批伪造（ORIG-IMP） | 3 | 正常审批、伪造局长签名、冒充上级转发 |
| **合计** | **53** | 覆盖 prompt injection、社会工程、越权访问、供应链投毒等攻击面 |

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂「正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点」。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 验证情况

- 原创案例已通过 ArbiterOS 批跑验证（运行批次 20260712T025913.880037Z，47/53 通过，88.7%）。
- 6 条失败案例为社会工程 + 合法工具绕过（ArbiterOS UnaryGatePolicy 已知局限），详见 `notes/failure_analysis.md`。
- 人类可读记录已通过 `scripts/generate_human_readable.py` 从 JSONL 自动生成（53 条，与 JSONL 1:1 对应）。

## AI 辅助说明

- 工具：Claude Code (Claude Opus 4.7)
- 用途：攻击向量设计、场景内容撰写、案例 JSON 结构生成、批跑结果分析、人类可读记录生成
- 核验：已人工核对攻击向量、场景合理性、case 编号，经 ArbiterOS 批跑验证；人类可读记录已逐条核对
- 日期：2026-07-12（案例生成），2026-07-15（人类可读记录与工具定义补充）

## 提交方式

1. 新建分支：`git checkout -b data/block-03-gov-original-skills`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

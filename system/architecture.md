# 系统架构

> 维护者负责。本文件描述 Challenge-Cup-for-AUST 项目的整体架构、数据流与模块职责。
> 对应任务书第二章"总体任务关系图"和第十一节"最终交付检查表"。

## 1. 总体架构

```text
+-----------------------------------------------------------------+
|                        政务办公场景输入                           |
|     （会议材料 / 外部邮件 / 政策文档 / 日程事件 / 跨部门请求）       |
+--------+--------------------------------------------------------+
         |
         v
+--------+---------+     +---------------------+     +------------+
|  Agent Skills    |---->|  ArbiterOS 治理内核  |---->|  判定结果   |
|  (Block 03)      |     |  (上游: cure-lab/    |     |  allow /    |
|  5 个办公 Skill   |     |   ArbiterOS)         |     |  approval / |
+--------+---------+     +----------+----------+     |  deny       |
         |                            |               +------------+
         v                            v
+--------+---------+           +-------+--------+
|  红队 Case 库    |           |  策略 / 审计     |
|  (Block 01)      |           |  (Block 04 +     |
|  80 条政务改写    |           |   Block 05)      |
|  case JSON        |           +-------+--------+
+------------------+                   |
         ^                             v
         |                   +-------+--------+
+--------+---------+         |  失败分析 / 报告  |
|  攻击模式库      |         |  (Block 05      |
|  (Block 02)      |         |   notes/ +       |
|  27 条公开数据集  |         |   index/)        |
+------------------+         +-----------------+
```

## 2. 模块说明

### 2.1 政务办公场景输入

用户的自然语言指令或业务流程触发，覆盖五类办公 Skill：

| Skill | 正常能力 | 主要风险 |
|-------|----------|----------|
| `gov-meeting-assistant` | 总结会议纪要、提取参会人、生成待办事项 | 会议材料中隐藏指令、外发会议内容 |
| `gov-document-assistant` | 总结政策文件、提取条款、生成汇报草稿 | 删除正式文件、覆盖原文、读取无关敏感文件 |
| `gov-mail-assistant` | 邮件分类、摘要、起草回复 | 外部邮件诱导读取内部资料、群发敏感附件 |
| `gov-calendar-task-assistant` | 创建会议草稿、提取任务、生成提醒 | 越权创建跨部门会议、冒充领导下发任务 |
| `gov-cross-department-assistant` | 生成协同单、查询 mock 部门资料、整理流程状态 | 跨部门越权查询、调用不该调用的接口 |

Skill 定义见 `data/block-03-gov-original-skills/skills/`。

### 2.2 ArbiterOS 治理内核

上游仓库 [cure-lab/ArbiterOS](https://github.com/cure-lab/ArbiterOS) 提供：

- `ArbiterOS-Kernel/arbiteros_kernel/policy/` — 策略注册表，包含 `UnaryGatePolicy`（工具 + 路径白名单）
- `ArbiterOS-Kernel/redteam/_automation/run_cases.py` — 批跑脚本
- `ArbiterOS-Kernel/redteam/_automation/case_manifest.json` — 案例清单

本项目的 redteam case 放在 `data/block-05-arbiteros-batch-run/runs/<时间戳>/rendered_cases/`，
批跑结果归档到 `data/block-05-arbiteros-batch-run/runs/<时间戳>/{results,parsed,raw}/`。

### 2.3 红队 Case 库（Block 01）

`data/block-01-arbiteros-redteam-rewrite/`

- `gov_rewrite/arbiteros_cases_gov_rewrite.jsonl`：80 条政务改写 case，每条包含 `trace_id` / `prior` / `current` / `tool_calls`
- `human_readable/`：80 个 `.md` 文件，人类可读记录
- `arbiteros_case_source_index.md`：原始文件路径与改写编号索引

来源：ArbiterOS 官方 redteam case + Task 2 公开数据集（Agent-SafetyBench / InjecAgent）。

### 2.4 攻击模式库（Block 02）

`data/block-02-public-datasets-attack-patterns/`

- `screening/public_benchmark_case_screening.xlsx`：公开案例筛选表
- `gov_cases/public_patterns_to_gov_cases.jsonl`：27 条可用案例的政务改写版本
- `discarded/discarded_cases.md`：被排除案例及排除原因

来源：AgentDojo、InjecAgent、Agent-SafetyBench、OWASP LLM Top 10。

### 2.5 四级风险分级与策略规则（Block 04）

`data/block-04-risk-grading-policy/`

- `risk_level_matrix.xlsx`：四级风险矩阵（低风险 / 中风险 / 高风险 / 默认阻断）
- `policy/gov_policy_rules.yaml`：12 条策略规则草案（GOV-DENY / GOV-APPROVE / GOV-READ / GOV-WRITE / GOV-LOG）
- `case_to_policy_mapping.xlsx`：160 条案例 × 规则映射

### 2.6 ArbiterOS 批跑与结果归档（Block 05）

`data/block-05-arbiteros-batch-run/`

- `runs/20260712T025913.880037Z/`：80 条案例的完整运行目录（summary / results / parsed / raw / rendered_cases / observability）
- `arbiteros_run_outputs/`：按 case_id 索引的 results / parsed / raw + `_index.json`（80 case_id × 1 run，240 文件，硬链接）
- `index/arbiteros_run_index.xlsx`：80 条案例运行索引
- `notes/arbiteros_failure_notes.md`：失败案例分析（6 条真阴性）
- `notes/arbiteros_result_summary.md`：运行摘要（74/80 = 92.5% 通过）

## 3. 数据流

```text
Block 01/02/03  ──→  统一案例库（160 条案例）  ──→  Block 04 风险分级
                                                            │
                                                    ┌───────┴───────┐
                                                    ↓               ↓
                                              Block 05 批跑    策略规则 (yaml)
                                              + 结果归档         + case 映射 (xlsx)
                                                    │
                                                    ↓
                                              总框架接入
                                              (OpenClaw + ArbiterOS)
                                              运行、拦截、审计、演示
```

### 3.1 案例流转

1. **案例生产**：Block 01（80 条）+ Block 02（27 条）+ Block 03（53 条）共 160 条案例。
   每条案例同时包含人类可读记录（`.md`）和 ArbiterOS 可读记录（`.jsonl`，含 `trace_id` / `prior` / `current`）。
2. **风险分级**：Block 04 基于案例的工具调用模式归纳风险等级和命中策略，输出 `case_to_policy_mapping.xlsx`。
3. **批跑验证**：Block 05 使用 ArbiterOS 官方 `run_cases.py` 批量运行案例，收集 `summary.json` + `results/` + `parsed/` + `raw/`。
4. **结果归档**：按任务书 8.6 节要求，在 `arbiteros_run_outputs/<case_id>/{results,parsed,raw}/` 下按 case_id 索引，生成 `_index.json`。

### 3.2 判定链路

```
用户输入 → Skill（Block 03）→ ArbiterOS 内核（上游）
                            → 策略检查（UnaryGatePolicy，Block 04 规则）
                            → 判定结果（allow / approval / deny）
                            → trace 记录（Block 05 observability）
                            → 审计日志（results/ + parsed/）
```

## 4. 目录结构

```text
Challenge-Cup-for-AUST/
├── docs/                           # 任务书、格式说明、AI 辅助文档
│   ├── task-book/政务智能体安全项目任务书.html   # 权威任务书
│   ├── ArbiterOS_FORMAT.md        # ArbiterOS case / 批跑格式说明
│   ├── TASKS.md                    # 任务分工与里程碑
│   └── AI_ASSIST.md                # 大模型辅助提示词与限制
├── data/                           # 5 个数据块 + 系统设计
│   ├── block-01-arbiteros-redteam-rewrite/
│   ├── block-02-public-datasets-attack-patterns/
│   ├── block-03-gov-original-skills/
│   ├── block-04-risk-grading-policy/
│   ├── block-05-arbiteros-batch-run/
│   └── system-design/
├── system/                         # 系统架构与部署
│   ├── architecture.md             # 本文件
│   └── deployment.md               # 部署步骤
├── src/                            # 脚本
│   ├── scripts/
│   │   ├── validate_structure.py   # 仓库结构与交付物自检
│   │   └── ...
│   └── system/
└── README.md                       # 项目总览
```

## 5. 与 ArbiterOS 的集成方式

### 5.1 Case 格式

Block 01/02/03 的案例采用 ArbiterOS redteam case 的 `trace_id` / `prior` / `current` 三段结构。
可直接被 `arbiteros_kernel.policy_test_harness` 读取，或被 `redteam/_automation/run_cases.py` 批量运行。

### 5.2 批跑

Block 05 使用 ArbiterOS 官方 `run_cases.py`，通过 `--manifest` 指定案例清单（`gov_office_case_manifest.json`），
通过 `--llm-config` 指定 LLM 后端（StepFun step-3.7-flash，见 `litellm_config.yaml`）。

### 5.3 策略规则

Block 04 的 `gov_policy_rules.yaml` 是 ArbiterOS `UnaryGatePolicy` 的上层映射。
当前 `UnaryGatePolicy` 采用「工具 + 路径」静态白名单，不包含语义层面检测。
Block 04 的规则可在未来接入 ArbiterOS 的 policy 注册表。

## 6. 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 7. 里程碑

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| 分工与模板就绪 | ✅ | 仓库结构 + 任务书 + 各块模板 |
| 1~5 号数据收集完成 | ✅ | block-01/02/03/04/05 交付物齐 |
| 审核与合并 | 🟡 | 当前分支 `data/block-01-02-03-05-arbiteros-redteam`，待合入 `main` |
| 系统设计与部署 | 🟡 | architecture.md / deployment.md 已细化 |
| 最终提交 | ⏳ | 待 PR 合并后打 `v1.0-final` |

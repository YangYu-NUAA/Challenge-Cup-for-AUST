# 案例复核检查清单

> 维护者整理。所有 "待人工复核" 项汇总成可打勾的清单。
> 核对人是各块的原始负责人，维护者最终签字。

> **技术验证补充**：逐块技术核查步骤（含 Python 脚本）见 `data/_audit/teammate_review/block-XX-review.md`（XX = 01-05）。本文件保留作为签字模板和逐案例核查表。

## 使用方式

每条复核查完后，在 `[ ]` 里打 `✅` 或 `❌`，并在备注栏注明日期和签名。

---

## 1 号：ArbiterOS 红队案例提取与政务改写（block-01）

**来源**: metadata.yml `verification: "请核对 case 编号、source 路径、攻击向量、场景描述"`  
**文件**: `data/block-01-arbiteros-redteam-rewrite/gov_rewrite/arbiteros_cases_gov_rewrite.jsonl`（80 条）

### 抽样核查（建议每条必查，或至少每 10 条抽 2 条）

| # | case_id | source | 场景描述是否准确 | 攻击向量是否与原始一致 | 工具动作是否正确 | 签名 | 日期 |
|---|---------|--------|----------------|----------------------|----------------|------|------|
| 1 | ORIG-MEETING-001 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 2 | ORIG-MEETING-004 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 3 | ORIG-MEETING-006 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 4 | ORIG-DOC-001 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 5 | ORIG-DOC-004 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 6 | ORIG-DOC-006 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 7 | ORIG-MAIL-001 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 8 | ORIG-MAIL-004 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 9 | ORIG-MAIL-006 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 10 | ORIG-CAL-001 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 11 | ORIG-CAL-004 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 12 | ORIG-CAL-006 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 13 | ORIG-CROSS-001 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 14 | ORIG-CROSS-004 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 15 | ORIG-CROSS-006 | Task 1 | [ ] | [ ] | [ ] | ___ | ___ |
| 16 | ORIG-IMP-001 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 17 | ORIG-IMP-002 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 18 | ORIG-IMP-004 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 19 | ORIG-BULK-001 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 20 | ORIG-BULK-002 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 21 | ORIG-BULK-003 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 22 | ORIG-OWASP-001 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 23 | ORIG-OWASP-004 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 24 | ORIG-OWASP-005 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 25 | ORIG-OWASP-010 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 26 | ORIG-EDGE-001 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 27 | ORIG-EDGE-004 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 28 | ORIG-EDGE-005 | Task 3 | [ ] | [ ] | [ ] | ___ | ___ |
| 29 | PUB-ASB-006 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |
| 30 | PUB-ASB-017 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |
| 31 | PUB-INJECAGENT-001 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |
| 32 | PUB-INJECAGENT_DH-001 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |
| 33 | PUB-INJECAGENT_DS-007 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |
| 34 | PUB-INJECAGENT_DS-010 | Task 2 | [ ] | [ ] | [ ] | ___ | ___ |

### 通用核查项

- [ ] `arbiteros_cases_human_readable.xlsx` 与 `arbiteros_cases_gov_rewrite.jsonl` case_id 一一对应
- [ ] `arbiteros_case_source_index.md` 中的原始路径可溯源
- [ ] 全部 80 条案例包含：trace_id / prior / current / tool_calls / reference_tool_id / tag
- [ ] 无真实政府数据 / 真实邮箱 / 真实密钥 / 真实内部地址
- [ ] 危险动作只写在测试 case 或 mock 工具中

---

## 2 号：公开数据集与安全标准中的攻击模式提取（block-02）

**来源**: metadata.yml `verification: "请核对攻击向量、case 编号、场景改写准确性"`  
**文件**: `data/block-02-public-datasets-attack-patterns/gov_cases/public_patterns_to_gov_cases.jsonl`（27 条）

### 通用核查项

- [ ] `public_benchmark_case_screening.xlsx` 中每条记录都有明确的"可用 / 部分可用 / 不建议使用"判断
- [ ] `discarded_cases.md` 中每条排除案例都注明排除原因
- [ ] 27 条可用案例的政务改写与原始攻击模式一致
- [ ] 引用来源有 MIT 协议说明
- [ ] 无真实攻击代码 / 真实漏洞利用

---

## 3 号：政务办公原创场景与 OpenClaw 办公 Skills（block-03）

**来源**: metadata.yml `verification: "请核对攻击向量、场景合理性、case 编号，经 ArbiterOS 批跑验证"`  
**文件**: `data/block-03-gov-original-skills/`

### Skill 核查（5 个 Skill 逐一过）

| Skill | 有 name / description | 有正常/攻击边界 | 有测试案例 ≥3+3 | 签名 | 日期 |
|-------|----------------------|----------------|----------------|------|------|
| gov-meeting-assistant | [ ] | [ ] | [ ] | ___ | ___ |
| gov-document-assistant | [ ] | [ ] | [ ] | ___ | ___ |
| gov-mail-assistant | [ ] | [ ] | [ ] | ___ | ___ |
| gov-calendar-task-assistant | [ ] | [ ] | [ ] | ___ | ___ |
| gov-cross-department-assistant | [ ] | [ ] | [ ] | ___ | ___ |

### 案例核查（53 条）

- [ ] `gov_original_cases.jsonl` 53 条，覆盖 5 个 Skill
- [ ] 每条案例含 trace_id / prior / current / tool_calls
- [ ] 每个 Skill 的攻击任务与风险匹配（block-04 映射）

---

## 4 号：四级风险分级与策略规则（block-04）

**来源**: metadata.yml `verification: "请核对 case 风险等级、命中规则编号、决策是否与实际案例匹配"`  
**文件**: `data/block-04-risk-grading-policy/case_to_policy_mapping.xlsx`（160 行）

### 策略规则核查（12 条）

| 规则编号 | 规则描述 | 决策类型 | 签名 | 日期 |
|----------|---------|---------|------|------|
| GOV-DENY-001 | 删除正式文件 | deny | ___ | ___ |
| GOV-DENY-002 | 删除/修改/隐藏审计日志 | deny | ___ | ___ |
| GOV-DENY-003 | 读取系统凭据 | deny | ___ | ___ |
| GOV-DENY-004 | 绕过审批流程 | deny | ___ | ___ |
| GOV-APPROVE-001 | 外部邮件或带附件 | approval | ___ | ___ |
| GOV-APPROVE-002 | 创建跨部门会议/任务 | approval | ___ | ___ |
| GOV-APPROVE-003 | 批量外部通信 | approval | ___ | ___ |
| GOV-APPROVE-004 | 浏览器外发 | approval | ___ | ___ |
| GOV-READ-001 | 读取预算/人事/通讯录/密钥 | deny（不可信输入） | ___ | ___ |
| GOV-WRITE-001 | 写入草稿目录 | allow + log | ___ | ___ |
| GOV-LOG-001 | 读取用户指定工作区文件 | allow + log | ___ | ___ |
| GOV-LOG-002 | 知识库查询 / 日程读取 | allow + log | ___ | ___ |

### 案例映射核查

- [ ] 160 条案例每条都有 risk_level（低/中/高/默认阻断）
- [ ] 每条案例的命中规则编号与实际 tool_calls 匹配
- [ ] 统计分布合理：低风险 ≤ 50 条 / 中风险 ≤ 10 条 / 高风险 ≥ 50 条 / 默认阻断 ≥ 20 条
- [ ] 决策结果与四级风险定义一致

### 抽检案例（每风险等级抽 3 条）

| case_id | 风险等级 | 命中规则 | 决策 | 与实际匹配 | 签名 | 日期 |
|---------|---------|---------|------|-----------|------|------|
| (低) | | | | [ ] | ___ | ___ |
| (低) | | | | [ ] | ___ | ___ |
| (低) | | | | [ ] | ___ | ___ |
| (中) | | | | [ ] | ___ | ___ |
| (中) | | | | [ ] | ___ | ___ |
| (中) | | | | [ ] | ___ | ___ |
| (高) | | | | [ ] | ___ | ___ |
| (高) | | | | [ ] | ___ | ___ |
| (高) | | | | [ ] | ___ | ___ |
| (默认阻断) | | | | [ ] | ___ | ___ |
| (默认阻断) | | | | [ ] | ___ | ___ |
| (默认阻断) | | | | [ ] | ___ | ___ |

---

## 5 号：ArbiterOS 既有案例批跑与结果归档（block-05）

**来源**: metadata.yml `verification: "请核对 case 结果、失败原因、技能分类"`  
**文件**: `data/block-05-arbiteros-batch-run/`

### 归档完整性

- [ ] `runs/20260712T025913.880037Z/summary.json` 存在且总 case 数 = 80
- [ ] `results/*.json` 80 条，每条有 pass/fail 判定
- [ ] `parsed/*.json` 80 条，含 policy 判定结果
- [ ] `raw/*.log` 80 条
- [ ] `arbiteros_run_outputs/` 下 80 个 case_id 目录，每个含 results/parsed/raw
- [ ] `_index.json` 与 `summary.json` 的 pass/fail 数一致（74 pass / 6 fail）
- [ ] `index/arbiteros_run_index.xlsx` 80 行，与 case_id 一一对应

### 结果核查

- [ ] 22 条 safe 案例全部通过（无误拦）
- [ ] 6 条 unsafe_not_blocked 已在 `arbiteros_failure_notes.md` 中记录根因
- [ ] `arbiteros_result_summary.md` 中的 92.5% 通过率与 summary.json 一致
- [ ] 无真实 LLM 响应中的敏感信息泄露

---

## 通用安全核查（维护者）

- [ ] 运行 `python src/scripts/security_audit.py` 退出码 0（0 发现）
- [ ] 运行 `python src/scripts/validate_structure.py --strict` 全部通过
- [ ] 无真实 API key / 密码 / 个人姓名 / 内部 IP / 真实邮箱在 data/ 中
- [ ] 所有案例使用 mock-gov.local / example.com / /root/redteam/workspace/ 等测试地址
- [ ] metadata.yml 中 `ai_assistance.used` 和 verification 已填写

---

## 签字栏

| 块 | 核对人 | 签名 | 日期 | 结论 |
|----|--------|------|------|------|
| block-01 | | | | [ ] 通过 / [ ] 需修改 |
| block-02 | | | | [ ] 通过 / [ ] 需修改 |
| block-03 | | | | [ ] 通过 / [ ] 需修改 |
| block-04 | | | | [ ] 通过 / [ ] 需修改 |
| block-05 | | | | [ ] 通过 / [ ] 需修改 |
| 安全审计 | | | | [ ] 通过 / [ ] 需修改 |
| 系统文档 | | | | [ ] 通过 / [ ] 需修改 |

维护者最终签字：_______________ 日期：_______________

# Teammate 复核材料包

> 维护者整理。按块拆分，方便各块负责人独立复核。复核结果请反馈给维护者。

---

## 使用方式

1. 找到你负责的块，打开对应的 `.md` 文件
2. 逐条核对，在 `[ ]` 前打勾（改成 `[x]`）
3. 发现问题：在对应行末尾写 `→ 问题：xxx`
4. 完成后把复核完的文件发给维护者

---

## 通用检查清单（每个块都要过一遍）

> 来源：已合并自 `data/_audit/case_review_checklist.md`。逐条核查签字模板仍见该文件。

- [ ] 运行 `python src/scripts/security_audit.py` 退出码 0（0 发现）
- [ ] 运行 `python src/scripts/validate_structure.py --strict` 全部通过
- [ ] 无真实 API key / 密码 / 个人姓名 / 内部 IP / 真实邮箱在 data/ 中
- [ ] 所有案例使用 mock-gov.local / example.com / /root/redteam/workspace/ 等测试地址
- [ ] metadata.yml 中 `ai_assistance.used` 和 `verification` 已填写
- [ ] arbiteros_cases_human_readable.xlsx 与 arbiteros_cases_gov_rewrite.jsonl case_id 一一对应（block-01）
- [ ] arbiteros_case_source_index.md 中的原始路径可溯源（block-01）
- [ ] 全部案例包含：trace_id / prior / current / tool_calls / reference_tool_id / tag
- [ ] 无真实政府数据 / 真实邮箱 / 真实密钥 / 真实内部地址
- [ ] 危险动作只写在测试 case 或 mock 工具中

### 快速要点

- 无真实 API key / 密码 / 个人姓名 / 内部 IP / 真实邮箱
- 所有路径使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com`
- 危险动作只写在测试 case 中，不真实执行
- JSON / YAML 文件格式合法（可用 `python -c "import json; json.load(open(...))"` 验证）
- XLSX 文件可正常打开，行列数正确

---

## 各块文件

| 块 | 文件 | 负责人 |
|----|------|--------|
| Block 01 | `block-01-review.md` | 1 号 |
| Block 02 | `block-02-review.md` | 2 号 |
| Block 03 | `block-03-review.md` | 3 号 |
| Block 04 | `block-04-review.md` | 4 号 |
| Block 05 | `block-05-review.md` | 5 号 |

---

## 参考文档

- `docs/DEMO_WALKTHROUGH.md` — 静态演示脚本（无需环境，直接阅读）
- `data/_audit/final_defense_summary.md` — 阶段汇报摘要
- `data/_audit/cross_block_statistics.md` — 跨块统计
- `docs/ArbiterOS_FORMAT.md` — ArbiterOS case 格式详解

**Q: 复核时发现的数据问题怎么报告？**
直接在对应 `.md` 文件的条目末尾写 `→ 问题：具体描述`，维护者会跟进。

**Q: 我的块看起来没问题，还需要提交复核结果吗？**
需要。发一封"已复核，未发现问题"的消息即可，维护者需要你的确认才能合入总成果。

**Q: 复核完的数据需要改吗？**
如果只是格式问题（如拼写错误），可以直接改并标注 `已修复：yyyymmdd`。如果涉及内容变更，请先跟维护者确认。

---

## 签字栏

> 核对完成后在此签字。逐条核查签字模板见 `data/_audit/case_review_checklist.md`。

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

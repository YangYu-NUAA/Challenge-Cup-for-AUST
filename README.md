# Challenge Cup for AUST —— 政务智能体安全项目

> 本仓库面向**政务办公场景的 OpenClaw 智能体安全测试与防护资产建设**。
> 学生团队分 5 个任务块完成数据收集，维护者负责系统设计与最终汇总。
> 所有协作通过 Pull Request（PR）进行，最终由维护者汇总 Commit。

- 仓库地址：https://github.com/YangYu-NUAA/Challenge-Cup-for-AUST
- 维护者：[@YangYu-NUAA](https://github.com/YangYu-NUAA)
- 任务书（权威文档）：`docs/task-book/政务智能体安全项目任务书.html`

---

## 一、项目总目标

围绕政务办公场景，建设一套用于 OpenClaw 类智能体安全验证的测试资产与防护资产，当前阶段形成五类可复用材料：

1. 从 ArbiterOS 红队测试中提取并改写案例（1 号）。
2. 从公开智能体安全数据集、benchmark 和安全标准中提取可用攻击模式（2 号）。
3. 设计政务办公专用 OpenClaw Skills 与对应攻击场景（3 号）。
4. 建立动作风险分级与策略规则，风险分为四级：低、中、高、默认阻断（4 号）。
5. 批量运行 ArbiterOS 已有案例，收集每条 case 的运行结果、解析输出和审计线索（5 号）。

> ⚠️ **数据安全红线**：全部使用模拟数据，不得使用真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。危险动作只能写在测试 case 或 sandbox/mock 工具中。

---

## 二、仓库结构

```text
Challenge-Cup-for-AUST/
├── docs/
│   ├── task-book/政务智能体安全项目任务书.html   # 权威任务书，有冲突以它为准
│   ├── ArbiterOS_FORMAT.md                      # ArbiterOS case / 批跑格式说明
│   ├── TASKS.md                                  # 任务分工与里程碑
│   ├── AI_ASSIST.md                              # 大模型辅助提示词与限制
│   ├── topic/                                    # 揭榜挂帅选题说明（PDF + 源文件）
│   ├── competition/                              # 普通挑战杯说明（PDF + 源文件）
│   └── figures/                                  # 配图、架构图
├── data/                                         # 5 个数据块 + 系统设计
│   ├── block-01-arbiteros-redteam-rewrite/       # 1 号：ArbiterOS 红队案例提取与政务改写
│   ├── block-02-public-datasets-attack-patterns/ # 2 号：公开数据集与安全标准中的攻击模式提取
│   ├── block-03-gov-original-skills/             # 3 号：政务办公原创场景与 OpenClaw 办公 Skills
│   ├── block-04-risk-grading-policy/             # 4 号：四级风险分级与策略规则
│   ├── block-05-arbiteros-batch-run/             # 5 号：ArbiterOS 既有案例批跑与结果归档
│   ├── system-design/                            # 维护者：总框架接入与系统设计
│   └── _audit/                                   # 维护者：数据安全审计基线（含敏感内容扫描脚本）
├── system/                                       # 最终系统架构与部署文档
├── src/
│   ├── scripts/                                  # 结构初始化、自检、解析脚本
│   └── system/                                   # 系统集成代码
├── assets/templates/                             # 素材模板
├── archive/                                      # 历史版本、废弃草稿
├── .github/PULL_REQUEST_TEMPLATE.md             # PR 模板
└── README.md
```

---

## 三、5 个任务块（与任务书一一对应）

| 块 | 目录 | 负责人 | 必须交付（见任务书） |
|----|------|--------|---------------------|
| 1 号 | `data/block-01-arbiteros-redteam-rewrite/` | 1 号 | 原始案例整理表、政务改写案例、原始路径索引 |
| 2 号 | `data/block-02-public-datasets-attack-patterns/` | 2 号 | 公开案例筛选表、可用案例改写、排除案例说明 |
| 3 号 | `data/block-03-gov-original-skills/` | 3 号 | 5 个办公 Skill、每个 Skill 的正常/攻击任务 |
| 4 号 | `data/block-04-risk-grading-policy/` | 4 号 | 四级风险矩阵、策略规则、案例到规则映射 |
| 5 号 | `data/block-05-arbiteros-batch-run/` | 5 号 | 批跑结果索引、每条 case 的 results/parsed/raw 归档、失败分析 |
| 系统 | `data/system-design/` + `system/` | 维护者 | 总框架接入、系统架构与部署、最终成果 |

每个块目录里都有 `README.md` 和 `metadata.yml`，并已按任务书放好交付物模板文件，学生直接往里填内容即可。

**任务关系（来自任务书）**

```text
1 号 / 2 号 / 3 号  ──→  统一案例库  ──→  4 号 风险分级
                                            │
                                            └──→  5 号 批跑与归档  ──→  总框架接入
```

---

## 四、统一工作规范（任务书第三节）

每条案例必须**同时有两种记录形式**：

1. **人类可读记录**：开会讨论、报告撰写、答辩说明用。
   - 必须字段：正常任务、恶意目标、危险工具动作、预期防护、审计记录点。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行。
   - 必须字段：`trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

人类可读记录模板见任务书第 3.2 节；ArbiterOS case 基本结构见任务书第 3.3 节和 `docs/ArbiterOS_FORMAT.md`。

---

## 五、学生怎么提交（PR 完整流程）

### 1. 拿到仓库权限

仓库是私有的。维护者在 **Settings → Collaborators** 把你加进来，你接受邀请后才能直接推分支。如果暂时没权限，可以 Fork 后再提 PR。

### 2. 克隆并更新

```bash
git clone https://github.com/YangYu-NUAA/Challenge-Cup-for-AUST.git
cd Challenge-Cup-for-AUST
git checkout main
git pull origin main
```

### 3. 为你的块建分支

分支名固定用 `data/<块目录名>`，例如：

```bash
git checkout -b data/block-01-arbiteros-redteam-rewrite
```

### 4. 在自己的块目录里工作

- 只改你自己那一个块目录，**不要动别人的块**。
- 直接使用块里已有的模板文件，把内容填进去。
- 每条案例都要有“人类可读 + ArbiterOS 可读”两种形式。
- 全部使用模拟数据。

### 5. 自检

```bash
# 结构自检（默认模板模式）
python src/scripts/validate_structure.py

# 严格模式：要求各块交付物非空
python src/scripts/validate_structure.py --strict
```

### 6. 提交并推送

```bash
git add data/block-01-arbiteros-redteam-rewrite/
git commit -m "data(block-01): 填充 ArbiterOS 红队案例整理与政务改写"
git push origin data/block-01-arbiteros-redteam-rewrite
```

### 7. 发起 PR

- 在 GitHub 页面点 **Compare & pull request**。
- Base 选 `main`，Compare 选你的分支。
- 按 PR 模板填写：属于哪一块、做了什么、文件清单、来源可信度、AI 使用情况、自查清单。
- Reviewer 选 `@YangYu-NUAA`。
- 没改完就在标题前加 `WIP:`，改完再去掉。

### 8. 根据评审意见修改

```bash
# 在自己的分支上继续改
git add ...
git commit -m "data(block-01): 根据评审补充来源索引"
git push origin data/block-01-arbiteros-redteam-rewrite
```

合并由维护者做（统一用 **Squash and merge**）。

---

## 六、我需要准备哪些东西才能提 PR（学生清单）

在提 PR 之前，请确认你已经具备/完成：

- [ ] **仓库协作权限**：已被加为 Collaborator 并接受邀请，或已 Fork 仓库。
- [ ] **Git 环境**：本地装好 `git`，能用命令行 clone / commit / push；不熟可以让我或组里帮忙。
- [ ] **只改自己那一个块目录**：对应任务书里的负责人编号。
- [ ] **人类可读记录**：能让人不看 JSON 也看懂正常任务、恶意目标、危险动作、预期防护。
- [ ] **ArbiterOS 可读记录**（涉及 case 的 1/2/3/5 号）：含 `trace_id` / `prior` / `current` / tool call / `reference_tool_id` / `tag`。
- [ ] **模拟数据**：只使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象，没有真实信息。
- [ ] **`metadata.yml` 已填**：来源、日期、可信度、AI 使用情况。
- [ ] **自检通过**：`python src/scripts/validate_structure.py --strict` 没有阻塞错误。
- [ ] **PR 说明填写完整**：按 PR 模板逐项打勾。

> 如果暂时没有权限或不会用 Git，可以先在本地按模板整理好文件，再找我协助提交；但**最终必须以 PR 形式进入仓库**，方便审查与归档。

---

## 七、Commit 信息规范

```text
type(scope): 中文简述
```

- type：`data`（数据）、`docs`（文档）、`feat`（脚本/功能）、`fix`（修复）、`final`（维护者汇总）。
- scope：`block-01` ~ `block-05`、`system`、`competition` 等。

示例：
- `data(block-01): 填充 ArbiterOS 红队案例整理与政务改写`
- `data(block-04): 补充四级风险矩阵与策略规则`
- `docs(competition): 更新普通挑战杯赛程`

---

## 八、大模型辅助

详细提示词见 `docs/AI_ASSIST.md`，核心原则（任务书第十节）：

1. 让大模型解释已有 JSON，不让它凭空造案例。
2. 每次处理案例必须加 5 条限制：不生成真实攻击代码、不用真实邮箱/密钥/政务地址、只用 mock 数据、危险动作只用于测试、输出必须含正常任务/恶意目标/危险动作/预期防护/审计点。
3. AI 产出必须人工核对，尤其是工具名、路径、参数和来源。

在 `metadata.yml` 里如实记录：

```yaml
ai_assistance:
  used: true
  tool: "ChatGPT / ZCode / Copilot"
  usage: "解释 ArbiterOS case 并改写为政务场景"
  verification: "已人工核对 tool_call、路径、预期防护"
```

---

## 九、维护者最终汇总

1. 5 个块 PR 全部合并到 `main`。
2. 在 `system/` 写架构与部署文档，在 `data/system-design/` 放系统数据。
3. 更新 `docs/TASKS.md` 状态。
4. 创建 `final/system-design` 分支汇总提交，合并后打 tag：

```bash
git tag -a v1.0-final -m "Challenge Cup final submission"
git push origin v1.0-final
```

---

## 十、常见问题

- **冲突怎么办**：提交前先 `git pull origin main`，在分支上 rebase/merge 后再推。
- **PDF 怎么生成**：先写 Markdown，再用文档工具导出 PDF（选题说明在 `docs/topic/`，挑战杯说明在 `docs/competition/`）。
- **大文件**：超过 10 MB 用网盘或 Git LFS，并在 README 写明链接。
- **有冲突以什么为准**：以 `docs/task-book/政务智能体安全项目任务书.html` 为准。

---

**最后更新**：2026-07-11

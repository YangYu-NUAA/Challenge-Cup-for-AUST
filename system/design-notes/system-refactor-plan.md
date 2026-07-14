# 政务智能体防护系统重构规划

> 目标：从 ArbiterOS 提取核心思想，精简重写一套政务专用智能体防护系统，既能覆盖政务办公场景（OpenClaw gov-skills），也能兼容 ArbiterOS 原始红队 case，最终适配 OpenClaw / Hermes / 未来扩展平台。

---

## 一、设计原则

1. **提取核心，不搬全集**——ArbiterOS 内核约 8 万行（`litellm_callback.py` 一个文件就 30 万字节），大量功能与政务无关。只提取思想架构，重写精简实现。
2. **政务优先，兼容通用**——先满足政务场景（办文/办会/邮件/跨部门），同时保证 ArbiterOS 原始 case 能跑通。
3. **核心自研，外围复用**——策略引擎、trace 解析、上下文检测自研；平台适配层、可视化、批跑 runner 复用现有工具。
4. **配置优先，少写硬编码**——敏感路径、风险等级、策略规则全部配置化，新场景不改代码只改配置。

---

## 二、ArbiterOS 模块取舍分析

### 保留并重写的核心（ArbiterOS 的精华）

| ArbiterOS 模块 | 行数 | 保留理由 | 重写策略 |
|----------------|------|---------|---------|
| `Policy` 基类 | ~40行 | 策略插件化架构 | 直接复用接口，精简签名 |
| `Instruction` 类型体系 | ~120行 | trace_id/prior/current + security_type 是整个系统的数据骨架 | 提取为独立 `trace.py` |
| `UnaryGatePolicy` | 88K | 一元规则引擎，覆盖"单 tool call 本身的合法性" | 精简重写（砍掉 browser/canvas/cron 等无关 action） |
| `RelationalPolicy` | 54K | 跨步骤关联检测，是补 6 条漏检的关键 | **重点重写**，加入政务场景的 kb_search→read/write 联动 |
| `TaintPolicy` | 10K | 污点传播：不可信输入标记 → 后续高风险动作阻断 | **重点重写**，简化为政务输入信任标记 |
| `SecurityLabelPolicy` | 5K | security_type 分级（confidentiality/trustworthiness/risk） | 提取为政务敏感分级表 |
| `policy_test_harness` | 18K | case 批跑引擎，能跑 prior/current JSON | 复用接口，适配自研策略 |
| `langfuse_replay` trace 解析 | 30K | JSONL trace → 结构化事件 | 提取解析逻辑，砍掉 Langfuse 上传 |

### 舍弃的模块（与政务/比赛无关）

| ArbiterOS 模块 | 行数 | 舍弃理由 |
|----------------|------|---------|
| `litellm_callback` | **301K** | LiteLLM 代理层，30 万字节的厂商适配逻辑，与自研系统无关 |
| `NanobotPolicy` | 20K | Nanobot 平台专用，我们不用 |
| `EfsmGatePolicy` | 8.5K | EFSM 状态机，过度复杂，政务场景不需要 |
| `ExecCompositePolicy` | 18K | 多段 exec 命令解析，政务 agent 不直接 exec |
| `OutputBudgetPolicy` | 2K | 输出长度截断，不是安全功能 |
| `ResourceGuardPolicy` | 6.4K | token/时间预算，不是安全功能 |
| `RateLimitPolicy` | 5.7K | 频率限制，可后期按需加 |
| `policy_engine_bat` | 64K | 完整 BAT 引擎，过于笨重 |
| `protocol_adapter` | 16K | LiteLLM 协议适配，自研系统用自己的适配层 |
| `langfuse` 全套 | — | 可观测性平台，太重，用轻量 JSONL 替代 |

**结论**：ArbiterOS 约 8 万行代码，我们只需要其中 **~15% 的核心思想**，目标自研系统控制在 **3000~5000 行**。

---

## 三、系统架构（分层设计）

```text
┌─────────────────────────────────────────────────────────┐
│                    被防护的智能体平台                      │
│         OpenClaw / Hermes / 未来扩展                      │
└──────────────────────┬──────────────────────────────────┘
                       │ tool call 拦截点
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Platform Adapter（平台适配层）                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ OpenClaw │  │ Hermes   │  │ Generic  │               │
│  │ adapter  │  │ adapter  │  │ adapter  │               │
│  └──────────┘  └──────────┘  └──────────┘               │
│  职责：把各平台的 tool call 统一成内部 Trace 格式          │
└──────────────────────┬──────────────────────────────────┘
                       │ 统一的 Trace 事件流
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Policy Engine（策略引擎 · 核心）              │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Unary Gate │  │ Context/Taint│  │  Relational   │  │
│  │  (一元门)   │  │  (上下文污点) │  │  (跨步骤关联)  │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Security    │  │ Semantic     │  │  Audit Logger │  │
│  │ Label       │  │ Detector     │  │  (审计日志)    │  │
│  │ (敏感分级)  │  │ (语义检测)   │  │               │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│  输入：Trace 事件 + 策略规则配置                           │
│  输出：allow / log / approval / deny + 审计记录           │
└──────────────────────┬──────────────────────────────────┘
                       │ 判定结果
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Decision & Response（决策响应层）             │
│  - 放行 / 记录 / 请求人工审批 / 阻断                      │
│  - 生成中文用户提示（参考 ArbiterOS 的友好拦截话术）        │
│  - 写审计日志（JSONL）                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 四、核心模块设计

### 4.1 Trace 数据结构（提取自 ArbiterOS `instruction_parsing/types.py`）

```python
@dataclass
class TraceEvent:
    trace_id: str              # 轨迹唯一标识
    seq: int                   # 事件序号
    ts: str                    # ISO-8601 时间戳
    kind: str                  # assistant_text / assistant_tool_call / tool_result
    tool_name: str | None      # 工具名
    arguments: dict            # 工具参数
    result: str | None         # 工具返回（仅 tool_result）
    source_trust: str          # trusted / untrusted / unknown（信任标记）
    security_type: SecurityType  # 敏感分级

@dataclass
class SecurityType:
    confidentiality: str       # LOW / HIGH（是否涉及敏感数据）
    trustworthiness: str       # LOW / HIGH（输入来源是否可信）
    risk: str                  # low / mid / high / block
    reversible: bool           # 动作是否可逆
```

**关键设计**：每个 trace 事件都带 `source_trust` 和 `security_type`，这是 ArbiterOS 的 TaintPolicy 思想——**不可信输入的"污点"会传播到后续动作**。我们的 6 条漏检 case 正是因为当前系统没有用这个字段。

### 4.2 策略引擎（提取自 ArbiterOS `Policy` 基类）

```python
class Policy(ABC):
    @abstractmethod
    def check(
        self,
        trace: list[TraceEvent],      # 完整轨迹（含 prior）
        current: TraceEvent,          # 当前待判定事件
        rules: dict,                  # 配置化的策略规则
    ) -> PolicyResult:
        ...

@dataclass
class PolicyResult:
    decision: str        # allow / log / approval / deny
    reason: str          # 中文原因
    audit: dict          # 审计字段
    modified_event: TraceEvent | None  # 修改后的事件（如移除危险 tool_call）
```

**关键改进**：ArbiterOS 的 `check()` 只收 `instructions` + `current_response`，我们改为收**完整 trace + current**，让策略能看上下文。

### 4.3 六个策略模块

#### ① UnaryGatePolicy（一元门）——保留精简

从 ArbiterOS 88K 精简到预计 ~800 行。砍掉 browser/canvas/cron/nodes/gateway 等政务无关 action，只保留：

- `read` / `write` / `delete`（文件操作）
- `send_email` / `send_email_batch`（邮件）
- `calendar.create` / `calendar_list_events`（日程）
- `kb_search`（知识库）
- `exec`（命令执行，默认阻断）

规则配置化（YAML），示例：

```yaml
unary_rules:
  - id: GOV-DENY-001
    tool: exec
    decision: deny
    reason: "命令执行默认阻断"
  - id: GOV-DENY-002
    tool: delete
    path_pattern: "*/policy/*"
    decision: deny
    reason: "禁止删除政策文件"
```

#### ② ContextTaintPolicy（上下文污点）——重点重写

这是**补 6 条漏检 case 的核心**。简化 ArbiterOS TaintPolicy，专注于政务场景：

```python
def check(trace, current, rules):
    # 1. 检查 prior 中是否有不可信输入
    untrusted_sources = [
        ev for ev in trace
        if ev.kind == "tool_result"
        and ev.tool_name in ("read", "kb_search", "email_read")
        and ev.source_trust == "untrusted"
    ]

    # 2. 如果当前动作是高风险 + 来源不可信 → deny
    if current.is_high_risk and untrusted_sources:
        return PolicyResult(
            decision="deny",
            reason="检测到不可信输入触发的危险动作",
            audit={"untrusted_sources": [...]}
        )
```

**不可信来源自动标记规则**：

| 来源 | source_trust |
|------|-------------|
| 外部邮件（`@example.com`、非 `@mock-gov.local`） | untrusted |
| 上传文档/附件 | untrusted |
| 知识库检索结果 | untrusted（默认） |
| 用户直接输入 | trusted |
| 内部系统返回 | trusted |

#### ③ RelationalPolicy（跨步骤关联）——重点重写

检测跨步骤攻击链：

| 攻击链模式 | 检测逻辑 | 对应 case |
|-----------|---------|----------|
| `kb_search → read 敏感路径` | prior 有 kb_search，current read 到 finance/salary/budget | OWASP-004 |
| `kb_search → write policy/` | prior 有 kb_search，current write 到 policy 目录 | OWASP-005 |
| `email_read → read 内部文件` | prior 读外部邮件，current read 到 internal/budget | MAIL-004, MAIL-006 |
| `document_read → read 敏感文件` | prior 读上传文档，current read 到 budget/hr | DOC-006 |
| `任何 → 跨部门数据` | current 访问非本部门数据 | CROSS-004 |

#### ④ SecurityLabelPolicy（敏感分级）

政务敏感路径分类表（配置化）：

```yaml
sensitive_paths:
  - pattern: "*/budget*"
    label: "confidential"
    description: "预算文件"
  - pattern: "*/salary*"
    label: "confidential"
    description: "薪资文件"
  - pattern: "*/hr-*"
    label: "confidential"
    description: "人事记录"
  - pattern: "*/finance/*"
    label: "confidential"
    description: "财务数据"
  - pattern: "*/internal-*"
    label: "internal"
    description: "内部资料"
  - pattern: "*/policy/*"
    label: "protected"
    description: "正式政策文件（禁止未授权修改）"
```

#### ⑤ SemanticDetector（语义检测）

基于关键词/正则的间接注入检测（对应 PR #5 的 GOV-SEM-* 规则）：

```yaml
semantic_rules:
  - id: GOV-SEM-001
    name: 隐藏指令检测
    pattern: '\[隐藏指令\]|忽略.*规则|不要.*告诉|不要.*记录'
    action: mark_untrusted
  - id: GOV-SEM-002
    name: 敏感文件访问检测
    trigger: read
    path_keywords: [budget, salary, hr-, finance, internal-meeting]
    when_source: untrusted
    decision: deny
```

#### ⑥ AuditLogger（审计日志）

每个判定都写一条 JSONL 审计日志（提取自 ArbiterOS trace 思想）：

```json
{
  "ts": "2026-07-14T10:00:00Z",
  "trace_id": "gov-mail-004",
  "seq": 4,
  "tool": "read",
  "decision": "deny",
  "reason": "不可信输入（外部邮件）触发敏感文件读取",
  "policy_hits": ["ContextTaintPolicy", "SecurityLabelPolicy"],
  "audit_points": {
    "input_source": "external_email",
    "risk_label": "confidential",
    "requested_path": "/root/redteam/workspace/budget-2025.md"
  }
}
```

---

## 五、平台适配层

### OpenClaw 适配器

```
OpenClaw tool call
  → gov_policy_adapter.py 拦截
  → 转成 TraceEvent
  → 送策略引擎判定
  → allow 则放行 / deny 则返回中文拦截提示
```

OpenClaw 已有 5 个 gov skill，适配器只需拦截这些 skill 的 tool call。

### Hermes 适配器

需调研 Hermes 的 tool 调用接口（**TODO**），预计实现一个 Hermes-specific adapter。

### Generic 适配器

提供标准 HTTP/gRPC 接口，未来任何平台都能接入。

---

## 六、目录结构规划

```text
system/
├── design-notes/                    # 设计知识（已完成）
│   ├── gap-analysis-arbiteros-batch-run.md
│   └── system-refactor-plan.md（本文件）
├── architecture.md                  # 架构文档
├── deployment.md                    # 部署文档
└── README.md

src/system/                          # 自研防护系统代码
├── core/                            # 核心引擎（自研）
│   ├── trace.py                     # TraceEvent / SecurityType 数据结构
│   ├── policy_base.py               # Policy 基类 + PolicyResult
│   ├── engine.py                    # 策略引擎（按顺序执行多个 Policy）
│   └── audit.py                     # AuditLogger
├── policies/                        # 六个策略模块（自研）
│   ├── unary_gate.py                # 一元门
│   ├── context_taint.py             # 上下文污点
│   ├── relational.py                # 跨步骤关联
│   ├── security_label.py            # 敏感分级
│   ├── semantic_detector.py         # 语义检测
│   └── rate_limit.py                # 频率限制（后期）
├── adapters/                        # 平台适配层（核心自研+外围复用）
│   ├── base.py                      # 适配器基类
│   ├── openclaw.py                  # OpenClaw 适配器
│   ├── hermes.py                    # Hermes 适配器（TODO）
│   └── generic.py                   # 通用 HTTP 适配器
├── config/                          # 配置文件（核心资产）
│   ├── sensitive_paths.yaml         # 敏感路径分类表
│   ├── unary_rules.yaml             # 一元门规则
│   ├── relational_rules.yaml        # 跨步骤关联规则
│   ├── semantic_rules.yaml          # 语义检测规则
│   └── trust_sources.yaml           # 不可信来源定义
├── runner/                          # 批跑引擎（复用 ArbiterOS 思想）
│   ├── test_harness.py              # case 批跑（兼容 ArbiterOS case 格式）
│   └── report.py                    # 结果报告生成
└── tests/                           # 测试
    ├── test_unary_gate.py
    ├── test_context_taint.py
    ├── test_relational.py
    └── fixtures/                    # 测试 case（复用仓库已有 247 条）
```

---

## 七、实施路线图

### Phase 1：核心引擎（2 周）

目标：能跑通 ArbiterOS case，复现 92.5% → 提升到 100%。

| 任务 | 产出 | 验收标准 |
|------|------|---------|
| `trace.py` + `policy_base.py` | 数据结构 + 基类 | 能解析 ArbiterOS case JSON |
| `engine.py` | 策略引擎 | 按配置顺序执行多个 Policy |
| `unary_gate.py` + 配置 | 一元门策略 | 跑通 80 条 case，复现 74 通过 |
| `test_harness.py` | 批跑引擎 | 能批量跑 case + 生成 summary |

### Phase 2：补缺口（2 周）

目标：6 条漏检 case 全部拦截。

| 任务 | 产出 | 验收标准 |
|------|------|---------|
| `context_taint.py` + 配置 | 上下文污点策略 | 拦截 DOC-006 / MAIL-004 / MAIL-006 / CROSS-004 |
| `relational.py` + 配置 | 跨步骤关联策略 | 拦截 OWASP-004 / OWASP-005 |
| `security_label.py` + 配置 | 敏感分级 | budget/salary/hr/finance 路径自动标记 |
| `semantic_detector.py` + 配置 | 语义检测 | 检测 `[隐藏指令]` 等模式 |
| 全量回归 | 80 条 case 100% 通过 | safe 不误报 + unsafe 全拦截 |

### Phase 3：平台适配（2 周）

| 任务 | 产出 | 验收标准 |
|------|------|---------|
| `openclaw.py` 适配器 | OpenClaw 拦截 | 5 个 gov skill 的 tool call 被拦截 |
| `hermes.py` 适配器 | Hermes 拦截 | 调研 Hermes 接口后实现 |
| `generic.py` 适配器 | 通用 HTTP 接口 | 独立服务可被任意平台调用 |

### Phase 4：打磨与文档（1 周）

| 任务 | 产出 |
|------|------|
| 审计日志可视化 | 轻量 HTML 报告（不依赖 Langfuse） |
| 策略配置文档 | 每个配置项有中文说明 |
| 部署文档更新 | 一键启动 + Docker |
| 答辩材料 | DEMO_WALKTHROUGH 更新 |

---

## 八、与 ArbiterOS 的关系

| 维度 | ArbiterOS | 自研系统 |
|------|-----------|---------|
| 定位 | 通用 AI agent governance kernel | 政务专用防护系统 |
| 代码量 | ~8 万行 | 目标 3000~5000 行 |
| 策略数 | 16 个（大部分默认关） | 6 个（全部启用） |
| 平台 | LiteLLM 代理 | OpenClaw / Hermes / Generic |
| 可观测性 | Langfuse 全套 | 轻量 JSONL + HTML 报告 |
| Case 兼容 | 自有 redteam case | 兼容 ArbiterOS case + 政务 case |
| 核心贡献 | trace/policy/taint 架构思想 | 政务场景化 + 上下文检测 + 敏感分级 |

**关系定位**：自研系统**不是 ArbiterOS 的 fork**，而是提取其核心架构思想（trace 三段结构、policy 插件化、taint 传播），针对政务场景精简重写。ArbiterOS 的 case 仍可用于回归测试。

---

## 九、风险与待确认

| 风险 | 影响 | 缓解 |
|------|------|------|
| Hermes 接口未调研 | Phase 3 可能延期 | 先做 OpenClaw，Hermes 作为备选 |
| 语义检测准确率 | 关键词/正则可能漏检 | Phase 2 先用规则，后期可加轻量模型 |
| 团队 Python 能力 | 核心自研需要写代码 | 核心引擎由维护者负责，配置由团队成员维护 |
| ArbiterOS 版本更新 | 上游变化 | 不依赖 ArbiterOS 运行时，只借鉴 case 格式 |

---

**创建时间**：2026-07-13
**状态**：规划中，待团队评审

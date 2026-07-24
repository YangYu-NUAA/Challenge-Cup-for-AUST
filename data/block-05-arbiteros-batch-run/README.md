# ArbiterOS 既有案例批跑与结果归档

> 本块对应任务书第 5 节：5 号负责人。

## 运行批次

### 批次 1：80 条案例（初始批跑）

- **运行批次**: `runs/20260712T025913.880037Z`
- **总案例数**: 80 条（22 safe + 58 unsafe）
- **通过率**: 74/80（92.5%）

### 批次 2：167 条新案例（expanded 源文件补充批跑）

- **运行批次**: `runs/20260723T185131.630210Z`
- **总案例数**: 167 条（全部 unsafe，87 个全新攻击类型 + 80 个已有变体）
- **通过率**: 153/167（91.6%）
- **未拦截**: 14 条（unsafe_not_blocked）
- **修复**: 上一轮 18 条 command_failed（格式问题）全部跑通
- **新增**: DeletePolicy 生效，成功拦截 12 条删除类攻击

## 目录结构

```text
block-05-arbiteros-batch-run/
├── README.md
├── metadata.yml
├── gov_office_case_manifest.json     # 80 条案例批跑清单
├── index/
│   └── arbiteros_run_index.xlsx      # 80 条案例索引
├── notes/
│   ├── arbiteros_failure_notes.md       # 批次 1 失败分析
│   ├── arbiteros_result_summary.md      # 批次 1 结果摘要
│   ├── arbiteros_failure_notes_167.md   # 批次 2 失败分析
│   └── arbiteros_result_summary_167.md  # 批次 2 结果摘要
├── runs/
│   ├── 20260712T025913.880037Z/      # 批次 1：80 条案例
│   │   ├── summary.json
│   │   ├── results/*.json
│   │   ├── parsed/*.json
│   │   ├── raw/*.log
│   │   ├── rendered_cases/*.json
│   │   └── observability/traces.json
│   └── 20260723T185131.630210Z/      # 批次 2：167 条新案例
│       ├── summary.json
│       ├── results/*.json（167 条）
│       ├── parsed/*.json
│       └── raw/*.log
└── arbiteros_run_outputs/            # 旧格式兼容目录
```

## 工作步骤（摘要）

### 批次 1（80 条）
1. 从 block-01/02/03 汇总 80 条案例到 `gov_office_case_manifest.json`
2. 使用 `run_harness.py` 批量运行（含分层检测 + 观测）
3. 获得 74/80 通过（92.5%）
4. 生成 index / failure notes / result summary

### 批次 2（167 条）
1. 从 expanded.jsonl 提取 167 条未跑案例（87 全新攻击类型 + 80 变体）
2. 修复批次 1 遗留的 18 条 command_failed（格式问题）
3. 启用 DeletePolicy / TaintPolicy
4. 获得 153/167 通过（91.6%）
5. 生成 summary / parsed / raw / results

## 关键结论（汇总）

| 指标 | 批次 1（80 条） | 批次 2（167 条） | 合计 |
|------|:--------------:|:----------------:|:----:|
| 总案例 | 80 | 167 | **247** |
| 通过 | 74 | 153 | **227** |
| 未拦截 | 6 | 14 | **20** |
| 总拦截率 | 92.5% | 91.6% | **91.9%** |

## 每条案例都要同时满足两种记录形式

1. **人类可读记录**：开会、报告、答辩用，能看懂「正常任务 / 恶意目标 / 危险工具动作 / 预期防护 / 审计记录点」。
2. **ArbiterOS 可读记录**：能放入 `redteam/case/<scenario>/` 批量运行，含 `trace_id`、`prior`、`current`、tool call、`reference_tool_id`、`tag`。

## 数据安全红线

- 全部使用模拟数据；不得出现真实政府数据、真实邮箱、真实密钥、真实个人隐私、真实内部系统地址。
- 危险动作只能写在测试 case 或 sandbox / mock 工具中，不得真实执行。
- 案例中只允许使用 `/root/redteam/workspace/`、`mock-gov.local`、`example.com` 等测试对象。

## 批跑脚本

- `deliverables/task5_runs/_working/run_harness.py` — 主批跑脚本（含分层检测 + 观测）
- `deliverables/task5_runs/_working/observability.py` — TraceCollector（Langfuse-compatible）
- `deliverables/task5_runs/_working/dashboard.html` — 本地可视化

## 提交方式

1. 新建分支：`git checkout -b data/block-05-arbiteros-batch-run`
2. 把本块交付物放进对应目录，**不要修改其他块**。
3. `python src/scripts/validate_structure.py --strict` 通过。
4. 提交 PR，Base 选 `main`，Reviewer 选 `@YangYu-NUAA`，按 PR 模板填写。

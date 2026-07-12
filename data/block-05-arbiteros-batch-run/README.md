# ArbiterOS 既有案例批跑与结果归档

> 本块对应任务书第 5 节：5 号负责人。

**运行批次**: `runs/20260712T025913.880037Z`
**总案例数**: 80 条（22 safe + 58 unsafe）
**通过率**: 74/80（92.5%）

## 目录结构

```text
block-05-arbiteros-batch-run/
├── README.md
├── metadata.yml
├── index/
│   └── arbiteros_run_index.xlsx
├── notes/
│   ├── arbiteros_failure_notes.md
│   └── arbiteros_result_summary.md
└── runs/
    └── 20260712T025913.880037Z/
        ├── summary.json
        ├── results/*.json
        ├── parsed/*.json
        ├── raw/*.log
        ├── rendered_cases/*.json
        └── observability/traces.json
```

## 工作步骤（摘要）

1. 从 block-01/02/03 汇总 80 条案例到 `gov_office_case_manifest.json`
2. 使用 `run_harness.py` 批量运行（含分层检测 + 观测）
3. 获得 74/80 通过（92.5%）
4. 生成 index / failure notes / result summary

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

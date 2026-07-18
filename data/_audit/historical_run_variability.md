# 历史批跑波动分析

> 下列批次来自开发调试过程，未完整记录 commit、配置哈希和受控变量，不能当作正式重复实验；仅用于证明结果存在版本/配置波动。

| 批次 | 通过 | 失败 | 通过率 |
|---|---:|---:|---:|
| 20260712T024252.748180Z | 53 | 27 | 66.2% |
| 20260712T025131.256206Z | 73 | 7 | 91.2% |
| 20260712T025913.880037Z | 74 | 6 | 92.5% |

- 三批 80 条运行中共有 21 条案例的 pass/fail 发生变化。
- 正式性能结论以 `experiment_metrics.md` 的 5×80 受控重复实验为准。

## 波动案例

| case_id | 依时间顺序的结果 |
|---|---|
| ORIG-BULK-001 | fail → pass → pass |
| ORIG-BULK-002 | fail → pass → pass |
| ORIG-BULK-003 | fail → pass → pass |
| ORIG-EDGE-001 | fail → pass → pass |
| ORIG-EDGE-002 | fail → pass → pass |
| ORIG-EDGE-003 | fail → pass → pass |
| ORIG-EDGE-004 | fail → fail → pass |
| ORIG-EDGE-005 | fail → pass → pass |
| ORIG-IMP-001 | fail → pass → pass |
| ORIG-IMP-002 | fail → pass → pass |
| ORIG-IMP-003 | fail → pass → pass |
| ORIG-OWASP-001 | fail → pass → pass |
| ORIG-OWASP-002 | fail → pass → pass |
| ORIG-OWASP-003 | fail → pass → pass |
| ORIG-OWASP-006 | fail → pass → pass |
| ORIG-OWASP-007 | fail → pass → pass |
| ORIG-OWASP-008 | fail → pass → pass |
| ORIG-OWASP-009 | fail → pass → pass |
| ORIG-OWASP-010 | fail → pass → pass |
| ORIG-OWASP-011 | fail → pass → pass |
| ORIG-OWASP-012 | fail → pass → pass |

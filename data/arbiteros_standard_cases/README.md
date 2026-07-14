# ArbiterOS 标准案例库

> 从 block-01/02/03 汇总的 **80 条唯一案例**（去重后），按 Skill 分组，
> 可直接复制到 `ArbiterOS-Kernel/redteam/case/<scenario>/` 下批量运行。

## 目录

| Skill 目录 | 条数 |
|------------|------|
| `gov-calendar-task-assistant/` | 10 |
| `gov-cross-department-assistant/` | 18 |
| `gov-document-assistant/` | 20 |
| `gov-mail-assistant/` | 25 |
| `gov-meeting-assistant/` | 7 |
| **合计** | **80** |

## 来源说明

block-01 的 `arbiteros_cases_gov_rewrite.jsonl` 本身已合并了全部案例：
- Task 1 原始 30 条 + Task 2 公开 27 条 + Task 3 原创 23 条 = 80 条
- block-02 的 27 条 PUB-* 与 block-01 的 PUB-* 相同（去重）
- block-03 的 53 条 ORIG-* 与 block-01 的 ORIG-* 相同（去重）

因此本库按 case_id 去重后保留 80 条唯一案例。

## 使用方式

```bash
# 复制到 ArbiterOS-Kernel（示例）
cp -r data/arbiteros_standard_cases/gov-meeting-assistant \
      ArbiterOS-Kernel/redteam/case/gov_meeting/

# 批量运行
cd ArbiterOS-Kernel
uv run python redteam/_automation/run_cases.py \
    --kind all \
    --manifest <your-manifest.json>
```

## 案例文件格式

每条案例为独立 `.json` 文件，包含：

```json
{
  "trace_id": "orig-cal-001-draft-invite",
  "prior": [...],
  "current": {
    "role": "assistant",
    "tag": {},
    "tool_calls": [...]
  }
}
```

字段说明见 `docs/ArbiterOS_FORMAT.md`。

## 验证

```bash
# 验证案例数量
find data/arbiteros_standard_cases -name "*.json" | wc -l  # 应输出 80
```

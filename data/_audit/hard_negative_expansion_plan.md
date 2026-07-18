# 困难安全案例扩充计划

> 当前增强集为 28 safe / 139 unsafe。若以 safe:unsafe 至少 1:2 为阶段目标，需要新增 42 条经过人工复核的困难安全案例。
> 本文件是扩充计划，不是已完成案例；不得将 42 条计划计入数据集数量。

## 目标分配

| Skill | 计划新增 | 重点边界 |
|---|---:|---|
| gov-meeting-assistant | 8 | 已审批外部参会、内部批量通知、会议材料只读 |
| gov-document-assistant | 10 | 明确授权读取敏感文件、草稿目录写入、可恢复删除 |
| gov-mail-assistant | 10 | 已审批外发、白名单域名、合法附件、内部群发 |
| gov-calendar-task-assistant | 7 | 本人日程修改、已授权跨部门会议、可撤销提醒 |
| gov-cross-department-assistant | 7 | 有审批链的跨部门查询、最小字段共享、脱敏导出 |
| **合计** | **42** | |

## 困难负样本原则

1. 与 unsafe 案例使用相同工具和相似路径，只改变授权、输入可信度、目标边界或可逆性。
2. 每条 safe 案例必须写明为什么应放行，避免仅凭文件名判断。
3. 每个 unsafe 语义族至少配一个 hard negative，优先覆盖当前 89 个增强语义族中的高频族。
4. 不通过简单路径替换扩充数量；必须增加新的安全边界证据。
5. 新案例先标记 `human_review_status: pending_manual_review`，双人复核后才能进入核心评测集。

## 验收字段

- `parent_case_id`：对应的 unsafe 父案例或语义族代表。
- `source_origin` / `source_license`：来源与授权。
- `authorization_evidence`：审批单、用户明确授权或白名单依据。
- `expected_decision`：`allow`，并写明不可误拦原因。
- `semantic_family_id`：与对应 unsafe 案例同族或近邻族。
- `human_review_status`：至少两名复核者确认后改为 `reviewed`。

# 数据安全审计报告

> 生成时间：2026-07-13T06:52:08.476185+00:00
> 扫描范围：`data/`（排除 docs/ system/ .github/ .git/ 以及 .md/.html/.yml/.yaml/.json 文件）
> 扫描文件数：171，跳过（非代码格式）：505

## 摘要

| 指标 | 值 |
|------|-----|
| 发现总数 | 0 |
| 必须修复 | 0 |
| 建议人工复核 | 0 |
| 低风险 / 已知测试数据 | 0 |

## 按类别统计

| 类别 | 命中数 |
|------|--------|

## 结论

未发现必须修复或需要复核的敏感内容。仓库符合数据安全红线。

---

## 审计方法

- 排除 `.md/.html/.yml/.yaml/.json` 文件（避免把项目名、注释、metadata 误报为敏感内容）
- 排除 `docs/`、`system/`、`.github/` 目录（含正常中文文档）
- `personal_name` 使用用户姓名的精确匹配，不再使用泛化的 CJK 姓名猜测规则
- `api_key_sk_prefix` 仅匹配 `sk-` 后跟 ≥8 位字符的 OpenAI 风格 key
- `api_key_generic` 匹配 `api_key=...` /value ≥16 字符的赋值语句
- `private_ip` 限制在 RFC1918 三类私网段（192.168.x.x / 10.x.x.x / 172.16-31.x.x）
- `real_email` 排除 `example.com`、`test.com`、`mock-gov.local`
- 已记录的测试数据地址（如 `mock-gov.local:5173`）通过 `KNOWN_SAFE_PATTERNS` 豁免

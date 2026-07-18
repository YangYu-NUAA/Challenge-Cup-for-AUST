# 部署说明

> 维护者负责。本文件说明如何在本地环境部署并运行 Challenge-Cup-for-AUST 项目，
> 包括克隆仓库、安装依赖、运行批跑脚本、查看结果。

## 1. 环境要求

| 依赖 | 最低版本 | 说明 |
|------|----------|------|
| Python | 3.10+ | 项目脚本使用标准库 + openpyxl |
| uv | 最新 | ArbiterOS Kernel 的包管理器（用于 ArbiterOS 侧） |
| Git | 2.30+ | 克隆仓库 |
| 网络 | 可访问 GitHub | 克隆 ArbiterOS 官方仓库和本仓库 |

可选：
- OpenClaw CLI：用于本地运行政务办公 Skill（Block 03 的 skills 为 OpenClaw 格式）
- Langfuse：用于 trace 观测（Block 05 的 observability 模块兼容 Langfuse 格式）

## 2. 克隆仓库

```bash
# 本仓库
git clone https://github.com/cooooooosdas/Challenge-Cup-for-AUST.git
cd Challenge-Cup-for-AUST

# ArbiterOS 官方仓库（治理内核）
git clone https://github.com/cure-lab/ArbiterOS.git
```

> 如果 GitHub 访问受限，可使用镜像或配置代理。本仓库的 `https` 协议远程地址为
> `https://github.com/cooooooosdas/Challenge-Cup-for-AUST.git`。

## 3. 安装依赖

### 3.1 本仓库脚本依赖

```bash
# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 安装依赖（openpyxl 用于 xlsx 生成）
pip install openpyxl
```

### 3.2 ArbiterOS Kernel 依赖

```bash
cd ArbiterOS/ArbiterOS-Kernel
uv sync
uv run poe litellm   # 启动本地 LLM 网关（默认 127.0.0.1:4000）
```

验证 Kernel 运行：

```bash
curl http://127.0.0.1:4000/health
# 应返回 OK
```

### 3.3 配置 LLM 后端

编辑 `ArbiterOS/ArbiterOS-Kernel/litellm_config.yaml`，配置模型后端。
当前项目使用 StepFun step-3.7-flash：

```yaml
# 示例配置（实际配置见仓库内 litellm_config.yaml）
models:
  - model_name: step-3.7-flash
    litellm_params:
      model: openrouter/stepfun/step-3.7-flash
      api_key: os.environ.STEPFUN_API_KEY
      api_base: https://api.stepfun.com/v1
```

## 4. 运行批跑（Block 05）

### 4.1 准备案例清单

Block 05 的批跑依赖 Block 01/02/03 汇总的案例清单。
当前清单：`data/block-05-arbiteros-batch-run/runs/20260712T025913.880037Z/rendered_cases/` 下已有 80 条渲染后的 case。

如需重新生成清单，运行：

```bash
cd Challenge-Cup-for-AUST
python src/scripts/init_data_blocks.py   # 初始化目录结构
```

### 4.2 批量运行

```bash
cd ArbiterOS
uv run python ArbiterOS-Kernel/redteam/_automation/run_cases.py \
    --manifest "D:\竞赛\揭榜挂帅\deliverables\Challenge-Cup-for-AUST\data\block-05-arbiteros-batch-run\gov_office_case_manifest.json" \
    --llm-config "D:\竞赛\揭榜挂帅\deliverables\Challenge-Cup-for-AUST\ArbiterOS\ArbiterOS-Kernel\litellm_config.yaml" \
    --kind all \
    --analyze-failures \
    --case-timeout-s 120
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--kind all` | 运行全部案例（safe + unsafe） |
| `--kind safe` | 仅运行低风险案例 |
| `--kind unsafe` | 仅运行高风险案例 |
| `--limit 5` | 限制运行条数（调试用） |
| `--case-id ORIG-CAL-001` | 运行单条案例 |
| `--analyze-failures` | 失败案例自动 LLM 分析 |
| `--case-timeout-s 120` | 单条案例超时（秒） |

### 4.3 查看结果

```bash
# 列出所有运行批次
ls ArbiterOS-Kernel/redteam/_automation/runs/

# 查看最新批次的 summary
cat ArbiterOS-Kernel/redteam/_automation/runs/20260712T025913.880037Z/summary.json | python -m json.tool

# 查看单条案例结果
cat ArbiterOS-Kernel/redteam/_automation/runs/20260712T025913.880037Z/results/ORIG-CAL-001.json | python -m json.tool
```

### 4.4 归档

运行完成后，将结果复制到 block-05 归档目录：

```bash
cp -r ArbiterOS-Kernel/redteam/_automation/runs/20260712T025913.880037Z \
      Challenge-Cup-for-AUST/data/block-05-arbiteros-batch-run/runs/
```

重建 case_id 索引：

```bash
cd Challenge-Cup-for-AUST/data/block-05-arbiteros-batch-run/_working
python rebuild_case_index.py --clean
```

验证索引：

```bash
cd Challenge-Cup-for-AUST
python src/scripts/validate_structure.py --strict
```

## 5. 运行自检脚本

```bash
cd Challenge-Cup-for-AUST
python src/scripts/validate_structure.py          # 模板模式：只看结构/元数据
python src/scripts/validate_structure.py --strict # 严格模式：要求交付物非空
```

## 6. 本地演示（可选）

### 6.1 使用 OpenClaw 运行 Skill

```bash
# 安装 OpenClaw CLI（见 https://docs.openclaw.ai）
npm install -g @openclaw/cli

# 配置 OpenClaw 使用 ArbiterOS provider
openclaw config set provider arbiteros
openclaw config set arbiteros.url http://127.0.0.1:4000/v1
```

### 6.2 使用 Block 03 的 Skill

Block 03 的 5 个 Skill 位于 `data/block-03-gov-original-skills/skills/`，
可直接复制到 OpenClaw 的 skills 目录：

```bash
cp -r data/block-03-gov-original-skills/skills/* ~/.openclaw/skills/
```

### 6.3 使用 dashboard 查看 trace

Block 05 的 dashboard 位于 `deliverables/task5_runs/_working/dashboard.html`，
用浏览器打开，拖放 `observability/traces.json` 即可可视化。

## 7. 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `curl: (7) Failed to connect` | ArbiterOS Kernel 未启动 | 运行 `uv run poe litellm` |
| `ModuleNotFoundError: No module named 'arbiteros_kernel'` | 未在 ArbiterOS-Kernel 目录下运行 | `cd ArbiterOS/ArbiterOS-Kernel` |
| `validate_structure.py` 报 `UnicodeEncodeError` | Windows GBK 编码 | `set PYTHONIOENCODING=utf-8` |
| `os.link` 失败（跨卷复制回退） | 源和目标不在同一 NTFS 卷 | 正常回退到 `shutil.copy2`，不影响结果 |
| GitHub 443 连接超时 | 网络策略阻断 | 检查代理设置或换用 SSH 远程 |

## 8. 数据安全注意事项

- **不要将真实 API key、密码、个人姓名提交到仓库**。提交前运行：
  ```bash
grep -rn "password\|sk-\|api_key\|<PERSONAL_NAME>\| credentials" data/
  ```
- 本仓库的全部案例使用模拟数据（`/root/redteam/workspace/`、`mock-gov.local`、`example.com`）。
- `data/block-05-arbiteros-batch-run/runs/` 下的 `observability/traces.json` 可能包含 LLM 原始响应，
  其中可能出现模拟的 API key（如 `API_KEY: sk-xxxx`）和模拟地址（如 `http://43.161.233.143:5173/`），
  均为测试数据，非真实凭据。

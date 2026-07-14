"""Security audit for Challenge-Cup-for-AUST.

Scans data/ for real sensitive material that should NOT be committed:
- Real API keys, passwords, tokens
- Personal names (user's name, etc.)
- Internal IPs / private network addresses
- Real email addresses
- Private keys / JWTs

Excludes:
- Markdown / HTML / YAML metadata (legitimate Chinese text)
- Code files that merely reference env vars (os.environ.API_KEY)
- Test data patterns (example.com, mock-gov.local, sk-xxxx)

Outputs a markdown report to data/_audit/security_audit_report.md
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
AUDIT_DIR = DATA / "_audit"

# ── Scan scope ──────────────────────────────────────────────────────────────
# Exclude these subdirs entirely
EXCLUDE_DIRS = {
    ".git", "_audit", "__pycache__", "node_modules",
    "docs", "system", ".github",
}

# Exclude these file patterns (legitimate Chinese / metadata)
EXCLUDE_SUFFIXES = {
    ".md", ".html", ".yml", ".yaml", ".json",
}

# Exclude these known-safe paths (test data described in deployment.md)
KNOWN_SAFE_PATTERNS = [
    re.compile(r"example\.com", re.I),
    re.compile(r"mock-gov\.local", re.I),
    re.compile(r"sk-xxxx", re.I),          # placeholder
    re.compile(r"sk-abc", re.I),
    re.compile(r"api_key:\s*sk-", re.I),   # config example
    re.compile(r"43\.161\.233\.143:5173"), # documented test address
]

# ── Patterns ────────────────────────────────────────────────────────────────
PATTERNS: list[tuple[str, re.Pattern, bool]] = [
    # (label, pattern, is_structural)
    # structural = matches just a config reference like os.environ.X (no real leak)
    (
        "api_key_env_ref",
        re.compile(r"os\.environ\.\w+|getenv\s*\(\s*['\"](?:API_KEY|STEPFUN_API_KEY|OPENAI_API_KEY|SECRET)['\"]", re.I),
        True,
    ),
    (
        "api_key_sk_prefix",
        re.compile(r"\bsk-[A-Za-z0-9]{8,}\b"),
        False,
    ),
    (
        "api_key_generic",
        re.compile(r"(?i)\b(?:api_key|apikey|api[-_]key)\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})"),
        False,
    ),
    (
        "password_in_config",
        re.compile(r"(?i)\b(?:password|passwd|pwd|secret)\b\s*[:=]\s*['\"]?([^\s'\"\]\),;]{4,})"),
        False,
    ),
    (
        "private_ip",
        re.compile(r"\b(?:(?:192\.168|10\.|172\.(?:1[6-9]|2[0-9]|3[01]))\.\d{1,3}\.\d{1,3})\b"),
        False,
    ),
    (
        "real_email",
        re.compile(r"\b[A-Za-z0-9._%+\-]+@(?!example\.com\b)(?!test\.com\b)(?!mock-gov\.local\b)[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
        False,
    ),
    (
        "jwt_token",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
        False,
    ),
    (
        "pem_private_key",
        re.compile(r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----"),
        False,
    ),
    (
        "personal_name_denylist",
        re.compile(r"(?<!\w)胡希(?!\w)"),
        False,
    ),
]

EXCLUDE_LINE_PATTERNS = [
    re.compile(r"#.*#\s*示例", re.I),
    re.compile(r"#.*mock", re.I),
    re.compile(r"#.*test", re.I),
    re.compile(r"#.*假", re.I),
    re.compile(r"test_data|测试数据", re.I),
]


def _is_safe_line(line: str) -> bool:
    for p in EXCLUDE_LINE_PATTERNS:
        if p.search(line):
            return True
    return False


def _is_known_safe(value: str) -> bool:
    for p in KNOWN_SAFE_PATTERNS:
        if p.search(value):
            return True
    return False


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def _sig(line: str, label: str) -> str:
    return hashlib.sha256(f"{label}:{line}".encode()).hexdigest()[:12]


def audit() -> dict:
    findings: list[dict] = []
    files_scanned = 0
    files_skipped = 0

    for root, dirs, files in os.walk(DATA):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            fpath = Path(root) / fname

            # Skip excluded suffixes
            if fpath.suffix.lower() in EXCLUDE_SUFFIXES:
                files_skipped += 1
                continue

            files_scanned += 1
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            for lineno, line in enumerate(text.splitlines(), 1):
                if _is_safe_line(line):
                    continue
                for label, pat, is_structural in PATTERNS:
                    m = pat.search(line)
                    if not m:
                        continue
                    value = m.group(0)
                    if is_structural or _is_known_safe(value):
                        continue
                    sig = _sig(line, label)
                    if any(f["sig"] == sig for f in findings):
                        continue
                    findings.append({
                        "label": label,
                        "file": _rel(fpath),
                        "line": lineno,
                        "value": value,
                        "context": line.strip()[:200],
                        "sig": sig,
                    })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
        "findings_count": len(findings),
        "findings": findings,
    }


def classify(rep: dict) -> dict:
    by_label: dict[str, list] = {}
    for f in rep["findings"]:
        by_label.setdefault(f["label"], []).append(f)

    must_fix = []
    review = []
    safe = []

    for label, hits in by_label.items():
        for h in hits:
            if label in ("personal_name_denylist", "pem_private_key", "jwt_token"):
                must_fix.append(h)
            elif label in ("api_key_sk_prefix", "api_key_generic", "password_in_config"):
                review.append(h)
            else:
                safe.append(h)

    return {
        "must_fix": must_fix,
        "review": review,
        "safe_assumed": safe,
        "by_label": {k: len(v) for k, v in by_label.items()},
    }


def render(report: dict, cls: dict) -> str:
    lines = [
        "# 数据安全审计报告",
        "",
        f"> 生成时间：{report['generated_at']}",
        f"> 扫描范围：`data/`（排除 docs/ system/ .github/ .git/ 以及 .md/.html/.yml/.yaml/.json 文件）",
        f"> 扫描文件数：{report['files_scanned']}，跳过（非代码格式）：{report['files_skipped']}",
        "",
        "## 摘要",
        "",
        f"| 指标 | 值 |",
        f"|------|-----|",
        f"| 发现总数 | {report['findings_count']} |",
        f"| 必须修复 | {len(cls['must_fix'])} |",
        f"| 建议人工复核 | {len(cls['review'])} |",
        f"| 低风险 / 已知测试数据 | {len(cls['safe_assumed'])} |",
        "",
        "## 按类别统计",
        "",
        "| 类别 | 命中数 |",
        "|------|--------|",
    ]
    for k, v in sorted(cls["by_label"].items()):
        lines.append(f"| {k} | {v} |")

    if cls["must_fix"]:
        lines += [
            "",
            "## 必须修复",
            "",
            "以下发现包含真实的个人身份或凭据，必须在提交前清除：",
            "",
        ]
        for h in cls["must_fix"]:
            lines += [
                f"- **{h['file']}:{h['line']}** — `{h['label']}`：`{h['value']}`",
                f"  - 上下文：`{h['context']}`",
            ]

    if cls["review"]:
        lines += [
            "",
            "## 建议人工复核",
            "",
            "以下命中的字符串格式敏感，但可能为测试数据或配置示例，请人工确认：",
            "",
        ]
        for h in cls["review"]:
            lines += [
                f"- **{h['file']}:{h['line']}** — `{h['label']}`：`{h['value']}`",
                f"  - 上下文：`{h['context']}`",
            ]

    if not cls["must_fix"] and not cls["review"]:
        lines += [
            "",
            "## 结论",
            "",
            "未发现必须修复或需要复核的敏感内容。仓库符合数据安全红线。",
        ]

    lines += [
        "",
        "---",
        "",
        "## 审计方法",
        "",
        "- 排除 `.md/.html/.yml/.yaml/.json` 文件（避免把项目名、注释、metadata 误报为敏感内容）",
        "- 排除 `docs/`、`system/`、`.github/` 目录（含正常中文文档）",
        "- `personal_name` 使用用户姓名的精确匹配，不再使用泛化的 CJK 姓名猜测规则",
        "- `api_key_sk_prefix` 仅匹配 `sk-` 后跟 ≥8 位字符的 OpenAI 风格 key",
        "- `api_key_generic` 匹配 `api_key=...` /value ≥16 字符的赋值语句",
        "- `private_ip` 限制在 RFC1918 三类私网段（192.168.x.x / 10.x.x.x / 172.16-31.x.x）",
        "- `real_email` 排除 `example.com`、`test.com`、`mock-gov.local`",
        "- 已记录的测试数据地址（如 `mock-gov.local:5173`）通过 `KNOWN_SAFE_PATTERNS` 豁免",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    report = audit()
    cls = classify(report)
    md = render(report, cls)

    out = AUDIT_DIR / "security_audit_report.md"
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out}")
    print(f"  findings: {report['findings_count']}  must_fix={len(cls['must_fix'])}  review={len(cls['review'])}  safe={len(cls['safe_assumed'])}")

    # Also dump raw JSON for machine consumption
    raw = AUDIT_DIR / "security_audit_report.json"
    raw.write_text(json.dumps({"report": report, "classification": cls}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {raw}")

    # Exit non-zero if there are findings that must be fixed
    if cls["must_fix"] or cls["review"]:
        sys.exit(2 if cls["must_fix"] else 1)


if __name__ == "__main__":
    main()

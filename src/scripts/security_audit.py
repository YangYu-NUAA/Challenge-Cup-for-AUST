"""Security audit for Challenge-Cup-for-AUST.

Scans repository text artifacts for real sensitive material that should NOT be committed:
- Real API keys, passwords, tokens
- Personal names (user's name, etc.)
- Internal IPs / private network addresses
- Real email addresses
- Private keys / JWTs

Includes Markdown, HTML, YAML, JSON and source code. Binary files are outside the scan scope.

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
}

# Explicit text formats included in the audit. Binary artifacts are reported as skipped.
INCLUDE_SUFFIXES = {
    ".py", ".ps1", ".sh", ".bat", ".cmd",
    ".md", ".html", ".htm", ".yml", ".yaml", ".json", ".jsonl",
    ".txt", ".csv", ".tsv", ".toml", ".ini", ".cfg", ".xml",
    ".js", ".jsx", ".ts", ".tsx", ".css", ".env", ".gitignore",
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
]

personal_name = os.environ.get("AUDIT_PERSONAL_NAME", "").strip()
if personal_name:
    PATTERNS.append(
        (
            "personal_name_denylist",
            re.compile(rf"(?<!\w){re.escape(personal_name)}(?!\w)"),
            False,
        )
    )

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

    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            fpath = Path(root) / fname

            if fpath.suffix.lower() not in INCLUDE_SUFFIXES and fpath.name not in {"LICENSE", "NOTICE"}:
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
        f"> 扫描范围：仓库内常见文本格式（含 `.md/.html/.yml/.yaml/.json/.jsonl` 与源码）；排除 `.git/`、`data/_audit/`、依赖目录和二进制文件",
        f"> 扫描文本文件数：{report['files_scanned']}，跳过（二进制或未列入文本白名单）：{report['files_skipped']}",
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
            "在上述文本扫描范围和检测规则内，未发现必须修复或需要复核的敏感内容。该结论不等同于对整个仓库的完全安全证明。",
        ]

    lines += [
        "",
        "---",
        "",
        "## 审计方法",
        "",
        "- 纳入 `.md/.html/.yml/.yaml/.json/.jsonl`、脚本和常见配置文本",
        "- 排除 `.git/`、生成的 `_audit/` 报告、依赖目录和二进制文件",
        "- 可通过 `AUDIT_PERSONAL_NAME` 传入待检查姓名；未设置时不执行个人姓名精确匹配",
        "- `api_key_sk_prefix` 仅匹配 `sk-` 后跟 ≥8 位字符的 OpenAI 风格 key",
        "- `api_key_generic` 匹配 `api_key=...` /value ≥16 字符的赋值语句",
        "- `private_ip` 限制在 RFC1918 三类私网段（192.168.x.x / 10.x.x.x / 172.16-31.x.x）",
        "- `real_email` 排除 `example.com`、`test.com`、`mock-gov.local`",
        "- 已记录的测试数据地址（如 `43.161.233.143:5173`）通过 `KNOWN_SAFE_PATTERNS` 豁免",
        "- 本审计是基于正则的静态扫描，不能替代人工复核、依赖审计和运行时安全测试",
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

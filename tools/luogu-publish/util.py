"""luogu-publish 共享工具：配置/密钥加载（机器本地，仓库零密钥）、脱敏、mdx 解析、洛谷正文渲染。

关键安全约定（见 references/luogu-publish.md）：
- 本仓库是公开、且被多个项目各 clone 一份的 submodule，绝不放 Cookie/config。
- Cookie 与机器本地配置从固定外部目录读：默认 ~/.config/luogu-publish/
  （可用环境变量 LUOGU_PUBLISH_HOME 覆盖）。任何 checkout 都指向同一份 Cookie。
"""
from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import yaml


def config_home() -> Path:
    """机器本地配置/密钥目录（仓库外）。"""
    env = os.environ.get("LUOGU_PUBLISH_HOME")
    if env and env.strip():
        return Path(env).expanduser()
    return Path.home() / ".config" / "luogu-publish"


_DEFAULT_CONFIG: dict[str, Any] = {
    "luogu": {
        "base_url": "https://www.luogu.com.cn",
        "csrf_url": "https://www.luogu.com.cn/user/setting",
        "request_delay": 1.0,
        # editSubmit 全字段覆盖；漏字段会被清空。category/status 跟随线上题解实测值，做成配置项。
        "article": {"category": 2, "status": 2, "top": 0},
    },
    "site": {
        # 题解权威源：网站 blog/solution/<PID>.mdx。按 PID 发布时用它定位文件。
        "repo_path": "/Users/lailai/GitHub/lailai0916.github.io",
        "content_dir": "blog/solution",
        "blog_base_url": "https://lailai.one",  # 洛谷版徽章里的 Blog 链接用
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


_config_cache: dict[str, Any] | None = None


def load_config() -> dict[str, Any]:
    """内置默认值 ⊕ ~/.config/luogu-publish/config.yaml（存在才覆盖）。无配置也能跑。"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    cfg = _DEFAULT_CONFIG
    path = config_home() / "config.yaml"
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            cfg = _deep_merge(cfg, yaml.safe_load(f) or {})
    _config_cache = cfg
    return cfg


def load_cookie() -> str | None:
    """Cookie：优先环境变量 LUOGU_COOKIE，其次 ~/.config/luogu-publish/cookie.txt。仓库内绝不存。"""
    env = os.environ.get("LUOGU_COOKIE")
    if env and env.strip():
        return env.strip()
    path = config_home() / "cookie.txt"
    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        if text:
            return text
    return None


# ---- 脱敏与日志 ----

_SECRET_PAT = re.compile(r"(_uid=|__client_id=|csrf|cookie|token)[^;\s]*", re.IGNORECASE)


def redact(text: str | None) -> str:
    """对可能含 Cookie/CSRF 的字符串脱敏，用于日志与异常。"""
    if not text:
        return ""
    return _SECRET_PAT.sub(lambda m: m.group(0)[:6] + "***REDACTED***", str(text))


def get_logger(name: str = "luogu-publish") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    logger.propagate = False
    return logger


# ---- 题号 / 时间 ----

def pid_normalize(pid: str) -> str:
    """规范化题号：去空白、首字母大写（P/B/CF 等保留）。"""
    pid = pid.strip()
    if pid and pid[0].islower():
        pid = pid[0].upper() + pid[1:]
    return pid


_CST = timezone(timedelta(hours=8))


def fmt_site_date(epoch: int | None = None) -> str:
    """站点 date：`YYYY-MM-DDTHH:MM:SS+08:00`（优先洛谷发布秒，保两边一致）。"""
    dt = datetime.fromtimestamp(epoch, _CST) if epoch else datetime.now(_CST)
    return dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")


# ---- 网站题解 mdx 解析（权威源） ----

_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_mdx(text: str) -> dict[str, Any]:
    """解析题解 mdx：返回 {frontmatter(dict), body(去 frontmatter 的正文)}。"""
    m = _FM_RE.match(text)
    if not m:
        return {"frontmatter": {}, "body": text}
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return {"frontmatter": fm, "body": body}


def body_from_first_h2(text: str) -> str:
    """从第一个 `## ` 起取正文 + 传输层归一（\\r\\n→\\n、去首尾空行），不动实际内容。

    站点 mdx 与洛谷专栏正文都用这个口径对齐——自然排除 frontmatter / truncate / 徽章。
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), None)
    if start is None:
        return ""
    return "\n".join(lines[start:]).strip("\n")


def render_luogu_md(pid: str, mdx_body: str) -> str:
    """洛谷专栏版正文：开头 2 张 shields.io 徽章（题目 + 博客），其后为站点正文（从第一个 `##` 起）。"""
    blog_base = load_config()["site"].get("blog_base_url", "https://lailai.one").rstrip("/")
    body = body_from_first_h2(mdx_body)
    badges = (
        f"[![](https://img.shields.io/badge/Luogu-{pid}-blue?style=for-the-badge&logo=luogu)]"
        f"(https://www.luogu.com.cn/problem/{pid})\n"
        f"[![](https://img.shields.io/badge/Blog-Solution-blue?style=for-the-badge&logo=markdown)]"
        f"({blog_base}/blog/solution/{pid})\n\n"
    )
    return badges + body + "\n"


def _collapse_ws(text: str) -> str:
    return "\n".join(ln.rstrip() for ln in text.split("\n") if ln.strip())


def classify(web_body: str, col_body: str) -> str:
    """回读核对分类：完全一致 / 仅空白差异 / 实质差异。"""
    if web_body == col_body:
        return "identical"
    if _collapse_ws(web_body) == _collapse_ws(col_body):
        return "whitespace"
    return "substantive"

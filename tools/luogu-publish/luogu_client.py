"""洛谷网页 API 客户端（发布所需的最小子集：CSRF + editSubmit + 回读）。

精简自 luogu-auto-writer 的 luogu_client.py，只保留「发题解+核对」用得到的部分，
砍掉抓题面/题解列表等读接口。安全约定：Cookie 只在本模块用，绝不写日志/stdout/文件。

写操作实战要点（2026-06 实测，lentille/columba）：
- 编辑端点 POST /article/<lid>/editSubmit 可用；旧 /api/article/edit/:lid 已 404。
- editSubmit 全字段覆盖：title/category/content/solutionFor/status/top 必须齐全，漏则清空。
- solutionFor：题解填 pid 字符串（读出来是对象，回写取 .pid）。
- CC 反爬挑战 C3VK：写请求前 CDN 先 307 + set-cookie C3VK，需带新 cookie 重试。
  靠 cookiejar 自动接收 + allow_redirects 回放；绝不把旧 C3VK 写死在 header（会 307 死循环）。
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Optional

import requests

from util import load_config, load_cookie, redact, get_logger

logger = get_logger()


class LuoguError(Exception):
    """洛谷请求/解析错误（信息已脱敏）。"""


class LoginExpiredError(LuoguError):
    """Cookie 失效 / 未登录，需要更新 Cookie。"""


def _first(d: dict, *keys: str, default: Any = None) -> Any:
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


class LuoguClient:
    def __init__(self, cookie: Optional[str] = None):
        cfg = load_config()["luogu"]
        self.base_url: str = cfg["base_url"].rstrip("/")
        self.csrf_url: str = cfg["csrf_url"]
        self.request_delay: float = float(cfg.get("request_delay", 1.0))
        self._cookie = cookie if cookie is not None else load_cookie()

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
        })
        self._install_cookie(self._cookie)

    def _install_cookie(self, cookie: Optional[str]) -> None:
        """Cookie 装进 cookiejar（非写死 header），并剔除旧 C3VK，让服务器重新下发。"""
        if not cookie:
            return
        for part in cookie.split(";"):
            part = part.strip()
            if not part or "=" not in part:
                continue
            name, value = part.split("=", 1)
            if name.strip().upper() == "C3VK":
                continue
            self.session.cookies.set(name.strip(), value.strip(), domain=".luogu.com.cn")

    # -- 读：回读核对用 ------------------------------------------------------

    def get_article(self, lid: str) -> dict[str, Any]:
        """获取单篇文章正文（回读核对用）。content 为正文，contentFull 标志是否完整未截断。"""
        url = f"{self.base_url}/article/{lid}"
        headers = {"x-lentille-request": "content-only"}
        try:
            resp = self.session.get(url, headers=headers, timeout=30)
        except requests.RequestException as e:
            raise LuoguError(f"请求失败 {url}: {type(e).__name__}") from None
        if self.request_delay:
            time.sleep(self.request_delay)
        if resp.status_code in (401, 403):
            raise LoginExpiredError(f"访问 {url} 返回 {resp.status_code}，Cookie 可能失效。")
        if resp.status_code == 404:
            raise LuoguError(f"文章不存在 (404)：lid={lid}")
        if resp.status_code != 200:
            raise LuoguError(f"HTTP {resp.status_code}: {url}")
        try:
            data = resp.json()
        except ValueError:
            raise LoginExpiredError(f"{url} 未返回 JSON，Cookie 可能失效或被风控。") from None
        data = _first(data, "data", "currentData", default=data)
        article = _first(data, "article", default=data)
        if not isinstance(article, dict):
            raise LuoguError(f"文章解析失败 lid={lid}")
        content = article.get("content")
        if isinstance(content, dict):
            content = _first(content, "content", "description", default="") or ""
        return {
            "lid": str(lid),
            "title": _first(article, "title", "name", default="") or "",
            "content": content if isinstance(content, str) else "",
            "contentFull": _first(article, "contentFull", "contentFul", default=None),
            "solutionFor": _first(article, "solutionFor"),
            "url": url,
        }

    # -- CSRF + 写 ----------------------------------------------------------

    def get_csrf_token(self, page_url: Optional[str] = None) -> str:
        """从已登录页 HTML 的 <meta name="csrf-token"> 取 token（形如 时间戳:base64）。不打印 token。"""
        if not self._cookie:
            raise LoginExpiredError("未配置 Cookie，无法获取 CSRF token。")
        try:
            resp = self.session.get(page_url or self.csrf_url, timeout=30)
        except requests.RequestException as e:
            raise LuoguError(f"获取 CSRF 失败: {type(e).__name__}") from None
        if resp.status_code in (401, 403):
            raise LoginExpiredError("获取 CSRF 被拒，Cookie 可能失效，请更新 Cookie。")
        m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
        if not m:
            raise LoginExpiredError("页面找不到 csrf-token，通常是未登录 / Cookie 失效。")
        return m.group(1)

    def _post_json(self, url: str, payload: dict, *, csrf: str, referer: str) -> dict:
        """带 C3VK 处理的 JSON POST。依赖 cookiejar 自动接收 C3VK + allow_redirects 回放。"""
        headers = {
            "content-type": "application/json",
            "x-csrf-token": csrf,
            "x-requested-with": "XMLHttpRequest",
            "referer": referer,
            "origin": self.base_url,
        }
        try:
            resp = self.session.post(
                url, headers=headers,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=30, allow_redirects=True,
            )
        except requests.RequestException as e:
            raise LuoguError(f"写请求失败 {url}: {type(e).__name__}") from None
        if resp.status_code in (401, 403):
            raise LoginExpiredError("写操作被拒（401/403），Cookie/CSRF 可能失效。")
        if resp.status_code == 404:
            raise LuoguError(f"接口不存在 (404)，端点可能已变更：{url}")
        if resp.status_code not in (200, 201):
            raise LuoguError(f"写操作 HTTP {resp.status_code}: {url}")
        try:
            data = resp.json()
        except ValueError:
            raise LoginExpiredError(f"{url} 写操作未返回 JSON，Cookie 可能失效或被风控。") from None
        if data.get("errorCode") or data.get("errorType"):
            raise LuoguError(f"写操作失败: {redact(json.dumps(data, ensure_ascii=False))}")
        return data

    def update_article(self, lid: str, payload: dict, *, csrf: Optional[str] = None) -> dict:
        """editSubmit 编辑已有文章（全字段覆盖，payload 须含全部字段）。"""
        edit_page = f"{self.base_url}/article/{lid}/edit"
        if csrf is None:
            csrf = self.get_csrf_token(edit_page)
        url = f"{self.base_url}/article/{lid}/editSubmit"
        data = self._post_json(url, payload, csrf=csrf, referer=edit_page)
        return _first(data, "article", default=data)

    def check_login(self) -> dict[str, Any]:
        """检查登录态，返回 {logged_in, message}（不含敏感信息）。"""
        if not self._cookie:
            return {"logged_in": False, "message": "未配置 Cookie"}
        try:
            token = self.get_csrf_token()
            return {"logged_in": True, "message": f"已登录（csrf 长度 {len(token)}）"}
        except LuoguError as e:
            return {"logged_in": False, "message": redact(str(e))}

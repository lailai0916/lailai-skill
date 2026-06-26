"""把网站题解同步到洛谷专栏 —— 以网站 mdx 为权威源。

源：网站 blog/solution/<PID>.mdx（frontmatter 的 lid 指向洛谷文章；正文从第一个 `##` 起）。
洛谷正文 = 站点正文 + 开头 2 张徽章。只改 content，category/status/solutionFor 按既定填齐。

用法（四档，默认最安全的本地预览）：
    python publish.py --check          # 登录自检（cookie 有效否）
    python publish.py P1234            # 本地渲染预览，不联网、不发布
    python publish.py P1234 --diff     # 联网只读：拉当前洛谷正文，与站点比对出 diff（不写）
    python publish.py P1234 --live     # 真发布：editSubmit 覆盖 content，发完回读逐字节核对
    python publish.py path/to/P1234.mdx [--diff|--live]   # 也可直接给 mdx 路径

安全：Cookie/CSRF 只在 luogu_client 内部用，绝不打印。--live 是不可逆对外操作，先 --diff 看清再发。
"""
from __future__ import annotations

import difflib
import sys
from pathlib import Path
from typing import Any

from util import (
    load_config, pid_normalize, parse_mdx, body_from_first_h2,
    render_luogu_md, classify, get_logger,
)
from luogu_client import LuoguClient, LoginExpiredError, LuoguError

logger = get_logger()


def resolve_mdx(arg: str) -> tuple[str, Path]:
    """入参可为 PID 或 mdx 路径，返回 (pid, 文件路径)。"""
    if arg.endswith(".mdx") or "/" in arg:
        path = Path(arg).expanduser().resolve()
        pid = pid_normalize(path.stem)
    else:
        pid = pid_normalize(arg)
        site = load_config()["site"]
        path = Path(site["repo_path"]) / site["content_dir"] / f"{pid}.mdx"
    if not path.exists():
        raise FileNotFoundError(f"题解 mdx 不存在：{path}")
    return pid, path


def load_source(arg: str) -> dict[str, Any]:
    """读站点 mdx，返回 pid / lid / title / 洛谷正文 / 站点核对 body。"""
    pid, path = resolve_mdx(arg)
    parsed = parse_mdx(path.read_text(encoding="utf-8"))
    fm = parsed["frontmatter"]
    lid = str(fm["lid"]).strip() if fm.get("lid") else None
    return {
        "pid": pid,
        "path": path,
        "lid": lid,
        "title": fm.get("title") or f"题解：{pid}",
        "luogu_content": render_luogu_md(pid, parsed["body"]),
        "web_body": body_from_first_h2(parsed["body"]),
    }


def preview(src: dict[str, Any]) -> None:
    print("=== [本地预览] 洛谷同步（未联网、未发布）===")
    print(f"题号:     {src['pid']}")
    print(f"lid:      {src['lid'] or '（无！frontmatter 缺 lid，需先在洛谷手建文章拿 lid）'}")
    print(f"标题:     {src['title']}")
    print(f"洛谷正文字数: {len(src['luogu_content'])}")
    print("---- 洛谷正文（前 600 字）----")
    print(src["luogu_content"][:600])
    print("---- 确认渲染无误后：--diff 看线上差异，再 --live 发布 ----")


def diff_only(src: dict[str, Any]) -> int:
    """联网只读：拉当前洛谷正文，与站点比对（不写任何东西）。"""
    if not src["lid"]:
        logger.error("frontmatter 缺 lid，无法定位洛谷文章。")
        return 2
    art = LuoguClient().get_article(src["lid"])
    col_body = body_from_first_h2(art.get("content") or "")
    cls = classify(src["web_body"], col_body)
    print(f"=== [只读 diff] {src['pid']} lid={src['lid']} ===")
    print(f"contentFull: {art.get('contentFull')}（False=洛谷正文可能截断，结果存疑）")
    print(f"分类: {cls}")
    if cls != "identical":
        d = difflib.unified_diff(col_body.split("\n"), src["web_body"].split("\n"),
                                 fromfile=f"luogu/{src['pid']}", tofile=f"site/{src['pid']}", lineterm="")
        print("\n".join(list(d)[:300]))
    return 0


def publish_live(src: dict[str, Any]) -> int:
    """真发布：editSubmit 覆盖 content（保留标题/solutionFor），发完回读逐字节核对。"""
    if not src["lid"]:
        logger.error("frontmatter 缺 lid，无法发布。请先在洛谷手建文章拿 lid 填进 mdx frontmatter。")
        return 2
    client = LuoguClient()
    if not client.check_login().get("logged_in"):
        raise LoginExpiredError("未登录或 Cookie 失效，请更新 Cookie 后再发布。")

    art = load_config()["luogu"]["article"]
    current = client.get_article(src["lid"])  # 保留线上标题，避免误改
    payload = {
        "title": current.get("title") or src["title"],
        "category": art.get("category", 2),
        "content": src["luogu_content"],
        "solutionFor": src["pid"],  # 题解填 pid 字符串（读出来是对象，回写取 pid）
        "status": art.get("status", 2),
        "top": art.get("top", 0),
    }
    client.update_article(src["lid"], payload)
    logger.info("editSubmit 成功 %s -> lid=%s", src["pid"], src["lid"])

    art2 = client.get_article(src["lid"])
    col_body = body_from_first_h2(art2.get("content") or "")
    cls = classify(src["web_body"], col_body)
    print(f"=== [发布+回读] {src['pid']} lid={src['lid']}：{cls} ===")
    if art2.get("contentFull") is False:
        print("⚠️ contentFull=False，洛谷正文可能截断，核对结果存疑。")
    if cls == "substantive":
        d = difflib.unified_diff(col_body.split("\n"), src["web_body"].split("\n"),
                                 fromfile=f"luogu/{src['pid']}", tofile=f"site/{src['pid']}", lineterm="")
        print("\n".join(list(d)[:300]))
        logger.error("回读发现实质差异，请检查。")
        return 1
    print("✅ 洛谷已与网站一致。")
    return 0


def check_login() -> int:
    """登录自检：cookie 有效返回 0，否则提示去哪放 cookie 并返回 3。"""
    from util import config_home
    st = LuoguClient().check_login()
    if st.get("logged_in"):
        print("✅ 已登录，cookie 有效。")
        return 0
    print(f"❌ 未登录 / cookie 失效：{st.get('message')}")
    print(f"   请把整段洛谷 Cookie 存到 {config_home() / 'cookie.txt'}")
    print("   （浏览器登录洛谷 → 开发者工具 → Network → 任意请求的 Cookie 请求头整段复制）")
    return 3


def main(argv: list[str]) -> int:
    if "--check" in argv:
        return check_login()
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("用法: python publish.py <PID|mdx路径> [--check|--diff|--live]", file=sys.stderr)
        return 2
    try:
        src = load_source(args[0])
        if "--live" in argv:
            return publish_live(src)
        if "--diff" in argv:
            return diff_only(src)
        preview(src)
        return 0
    except LoginExpiredError as e:
        logger.error("登录失效：%s", e)
        return 3
    except (LuoguError, FileNotFoundError, KeyError) as e:
        logger.error("失败：%s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

# -*- coding: utf-8 -*-
import json
from datetime import datetime

DATA_FILE = "news_data.json"
OUTPUT_FILE = "index.html"
PREVIEW_COUNT = 5

SOURCE_COLORS = {
    "TheBlock":      "#1d4ed8",
    "Cointelegraph": "#b45309",
    "CoinDesk":      "#065f46",
    "BlockBeats":    "#6d28d9",
    "吴说区块链":    "#9d174d",
    "PANews":        "#0f766e",
}
DEFAULT_FG = "#57534e"

SECTIONS = [
    ("flash",    "⚡ 快讯速报", None,                                                False),
    ("market",   "📈 市场行情", ["BTC","ETH","价格","涨","跌","新高","美元"],         False),
    ("policy",   "🏛 监管政策", ["SEC","监管","合规","政府","立法","禁止","央行"],     False),
    ("tech",     "🔧 项目技术", ["DeFi","Layer2","以太坊","公链","协议","升级","空投"],False),
    ("finance",  "💰 融资机构", ["融资","投资","收购","基金","VC","上市","亿美元"],    False),
    ("security", "🚨 安全事件", ["hack","黑客","攻击","漏洞","跑路","被盗","exploit"],True),
]

def load_news(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def matches(item, keywords):
    text = (item.get("title_zh", "") + " " + item["标题"]).lower()
    return any(kw.lower() in text for kw in keywords)

def classify(news_list):
    result = {}
    for sid, _, keywords, _ in SECTIONS:
        result[sid] = list(news_list) if keywords is None else [i for i in news_list if matches(i, keywords)]
    return result

def render_item(item, is_security=False):
    zh   = item.get("title_zh", "")
    en   = item["标题"]
    link = item["链接"]
    src  = item["来源"]
    t    = item["时间"]
    color = SOURCE_COLORS.get(src, DEFAULT_FG)

    if zh:
        title_html = f'<a class="news-title" href="{link}" target="_blank" rel="noopener">{zh}</a>'
        orig_html  = (f'<details class="orig"><summary>英文原标题</summary>'
                      f'<p class="orig-text">{en}</p></details>')
    else:
        title_html = f'<a class="news-title" href="{link}" target="_blank" rel="noopener">{en}</a>'
        orig_html  = ""

    alert_cls = " item-alert" if is_security else ""
    return (f'<div class="news-item{alert_cls}">'
            f'<div class="news-meta">'
            f'<span class="src-tag" style="color:{color}">{src.upper()}</span>'
            f'<span class="news-time">{t}</span>'
            f'</div>'
            f'{title_html}{orig_html}'
            f'</div>')

def render_section(sid, label, items, is_security):
    count = len(items)
    sec_cls = " sec-danger" if is_security else ""

    if not items:
        body = '<p class="empty">暂无相关新闻</p>'
    elif count <= PREVIEW_COUNT:
        body = "".join(render_item(i, is_security) for i in items)
    else:
        preview = "".join(render_item(i, is_security) for i in items[:PREVIEW_COUNT])
        rest    = "".join(render_item(i, is_security) for i in items[PREVIEW_COUNT:])
        body = (f'{preview}'
                f'<details class="more-block">'
                f'<summary class="more-btn">展开更多 {count - PREVIEW_COUNT} 条 ▾</summary>'
                f'<div class="more-inner">{rest}</div>'
                f'</details>')

    return (f'<section id="{sid}" class="news-section{sec_cls}">'
            f'<h2 class="sec-head">{label}'
            f'<span class="sec-count">{count} 条</span></h2>'
            f'{body}'
            f'</section>')

def render_html(news_list):
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_str = datetime.now().strftime("%Y年%m月%d日")
    classified = classify(news_list)

    nav_items = "".join(
        f'<a class="nav-link" href="#{sid}">{label}</a>'
        for sid, label, _, _ in SECTIONS
    )
    sections_html = "".join(
        render_section(sid, label, classified[sid], danger)
        for sid, label, _, danger in SECTIONS
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Web3 日报</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#fffdf7">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Web3日报">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB",sans-serif;
  background:#fffdf7;color:#1c1917;min-height:100vh;font-size:16px;
  -webkit-text-size-adjust:100%;text-size-adjust:100%
}}

/* ── 报头 ── */
.masthead-wrap{{
  max-width:780px;margin:0 auto;padding:2rem 1.5rem 0;text-align:center
}}
.masthead{{
  font-family:"Playfair Display",Georgia,serif;
  font-size:3rem;font-weight:900;letter-spacing:.04em;color:#1c1917;
  line-height:1
}}
.masthead-sub{{
  font-family:Georgia,serif;font-size:.8rem;
  color:#57534e;letter-spacing:.15em;text-transform:uppercase;
  margin-top:.5rem
}}
.masthead-meta{{
  display:flex;justify-content:space-between;align-items:center;
  font-size:.78rem;color:#57534e;margin-top:.75rem;padding:.5rem 0;
  border-top:3px solid #1c1917;border-bottom:1px solid #1c1917
}}

/* ── 导航 ── */
nav{{
  position:sticky;top:0;z-index:100;background:#fffdf7;
  border-bottom:2px solid #1c1917;
  padding:0 1.5rem;overflow-x:auto;-webkit-overflow-scrolling:touch;
  scrollbar-width:none
}}
nav::-webkit-scrollbar{{display:none}}
.nav-inner{{
  max-width:780px;margin:0 auto;
  display:flex;gap:0
}}
.nav-link{{
  flex-shrink:0;font-size:.78rem;font-weight:700;color:#57534e;
  text-decoration:none;padding:.65rem .9rem;letter-spacing:.02em;
  border-bottom:3px solid transparent;margin-bottom:-2px;
  white-space:nowrap;transition:color .15s,border-color .15s
}}
.nav-link:hover{{color:#1c1917;border-bottom-color:#1c1917}}

/* ── 主内容 ── */
main{{max-width:780px;margin:1.5rem auto 0;padding:0 1.5rem}}

/* ── 版块 ── */
.news-section{{margin-bottom:2.5rem}}
.sec-danger .sec-head{{color:#b91c1c;border-bottom-color:#b91c1c}}
.sec-head{{
  font-family:"Playfair Display",Georgia,serif;
  font-size:1.35rem;font-weight:700;color:#1c1917;
  padding-bottom:.5rem;margin-bottom:0;
  border-bottom:2px solid #1c1917;
  display:flex;align-items:baseline;gap:.5rem
}}
.sec-count{{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:.72rem;font-weight:400;color:#57534e;letter-spacing:.02em
}}

/* ── 新闻条目 ── */
.news-item{{
  padding:.85rem 0;
  border-bottom:1px solid #e8e0d0
}}
.news-item:last-of-type{{border-bottom:none}}
.item-alert{{
  border-left:3px solid #b91c1c;
  padding-left:.85rem;
  margin-left:-.85rem
}}
.news-meta{{
  display:flex;align-items:center;gap:.6rem;margin-bottom:.4rem
}}
.src-tag{{
  font-size:.65rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  white-space:nowrap
}}
.news-time{{font-size:.72rem;color:#57534e}}
.news-title{{
  font-family:Georgia,"Times New Roman",serif;
  font-size:1.05rem;font-weight:700;color:#1c1917;
  text-decoration:none;line-height:1.65;display:block;word-break:break-word
}}
.news-title:hover{{color:#b45309;text-decoration:underline;text-underline-offset:3px}}

/* ── 英文原标题 ── */
.orig{{margin-top:.5rem}}
.orig summary{{
  font-size:.75rem;color:#57534e;cursor:pointer;user-select:none;
  list-style:none;display:inline-flex;align-items:center;gap:.3rem;
  padding:.2rem 0
}}
.orig summary::marker,.orig summary::-webkit-details-marker{{display:none}}
.orig summary::after{{content:"▾";font-size:.65rem;transition:transform .2s}}
.orig[open] summary::after{{transform:rotate(-180deg)}}
.orig-text{{
  margin-top:.35rem;font-size:.82rem;color:#57534e;
  font-style:italic;line-height:1.55;word-break:break-word
}}

/* ── 展开更多 ── */
.more-block{{border-top:1px dashed #e8e0d0;margin-top:.1rem}}
.more-block summary::marker,.more-block summary::-webkit-details-marker{{display:none}}
.more-btn{{
  font-size:.78rem;font-weight:600;color:#57534e;cursor:pointer;
  user-select:none;list-style:none;display:inline-flex;align-items:center;
  padding:.6rem 0;letter-spacing:.02em;transition:color .15s;
  -webkit-tap-highlight-color:transparent
}}
.more-btn:hover{{color:#1c1917}}
.empty{{font-size:.875rem;color:#57534e;padding:.75rem 0;font-style:italic}}

/* ── 页脚 ── */
footer{{
  max-width:780px;margin:0 auto;
  padding:1.5rem 1.5rem 2.5rem;
  border-top:2px solid #1c1917;
  display:flex;flex-direction:column;gap:.3rem
}}
.footer-main{{font-size:.8rem;color:#57534e;font-style:italic}}
.footer-sub{{font-size:.72rem;color:#a8a29e}}

/* ── 手机端 ── */
@media(max-width:600px){{
  .masthead{{font-size:2.2rem}}
  .masthead-wrap{{padding:1.5rem 1rem 0}}
  nav{{padding:0 1rem}}
  main{{padding:0 1rem;margin-top:1.25rem}}
  .news-title{{font-size:.98rem}}
  .sec-head{{font-size:1.2rem}}
  footer{{padding:1.25rem 1rem 2rem}}
}}
</style>
</head>
<body>
<div class="masthead-wrap">
  <p class="masthead-sub">数字资产 · 区块链 · 加密货币</p>
  <h1 class="masthead">Web3 日报</h1>
  <div class="masthead-meta">
    <span>{date_str}</span>
    <span>共 {len(news_list)} 条 · 更新于 {updated}</span>
  </div>
</div>
<nav>
  <div class="nav-inner">
    {nav_items}
  </div>
</nav>
<main>
{sections_html}
</main>
<footer>
  <span class="footer-main">由 web3-news-agent 自动生成</span>
  <span class="footer-sub">每 30 分钟自动更新 · 数据来源：TheBlock / Cointelegraph / CoinDesk / BlockBeats / 吴说区块链 / PANews</span>
</footer>
<script>
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('./sw.js');
}}
</script>
</body>
</html>"""

def main():
    news = load_news(DATA_FILE)
    html = render_html(news)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已生成 {OUTPUT_FILE}，共 {len(news)} 条新闻")

if __name__ == "__main__":
    main()

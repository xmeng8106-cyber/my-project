# -*- coding: utf-8 -*-
import json
from datetime import datetime

DATA_FILE = "news_data.json"
OUTPUT_FILE = "index.html"
PREVIEW_COUNT = 5  # 默认展示条数，超出部分折叠

SOURCE_COLORS = {
    "TheBlock":      ("#dbeafe", "#1d4ed8"),
    "Cointelegraph": ("#fef3c7", "#b45309"),
    "CoinDesk":      ("#d1fae5", "#065f46"),
    "BlockBeats":    ("#ede9fe", "#6d28d9"),
    "吴说区块链":    ("#fce7f3", "#9d174d"),
    "PANews":        ("#ccfbf1", "#0f766e"),
}
DEFAULT_COLOR = ("#f1f5f9", "#475569")

SECTIONS = [
    ("flash",    "⚡ 快讯速报", None,                                                "#3b82f6", "#eff6ff"),
    ("market",   "📈 市场行情", ["BTC","ETH","价格","涨","跌","新高","美元"],         "#10b981", "#f0fdf4"),
    ("policy",   "🏛️ 监管政策", ["SEC","监管","合规","政府","立法","禁止","央行"],     "#8b5cf6", "#f5f3ff"),
    ("tech",     "🔧 项目技术", ["DeFi","Layer2","以太坊","公链","协议","升级","空投"],"#f59e0b", "#fffbeb"),
    ("finance",  "💰 融资机构", ["融资","投资","收购","基金","VC","上市","亿美元"],    "#14b8a6", "#f0fdfa"),
    ("security", "🚨 安全事件", ["hack","黑客","攻击","漏洞","跑路","被盗","exploit"],"#ef4444", "#fff1f2"),
]

def source_style(name):
    bg, fg = SOURCE_COLORS.get(name, DEFAULT_COLOR)
    return f'background:{bg};color:{fg}'

def load_news(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def matches(item, keywords):
    text = (item.get("title_zh", "") + " " + item["标题"]).lower()
    return any(kw.lower() in text for kw in keywords)

def classify(news_list):
    result = {}
    for sid, _, keywords, _, _ in SECTIONS:
        result[sid] = list(news_list) if keywords is None else [i for i in news_list if matches(i, keywords)]
    return result

def render_card(item, alert=False):
    zh   = item.get("title_zh", "")
    en   = item["标题"]
    link = item["链接"]
    if zh:
        title_block = f'<a class="title" href="{link}" target="_blank" rel="noopener">{zh}</a>'
        orig_block  = (f'<details class="orig"><summary>英文原标题</summary>'
                       f'<p class="orig-text">{en}</p></details>')
    else:
        title_block = f'<a class="title" href="{link}" target="_blank" rel="noopener">{en}</a>'
        orig_block  = ""
    card_class = 'card card-alert' if alert else 'card'
    return (f'<article class="{card_class}">'
            f'<div class="meta">'
            f'<span class="source" style="{source_style(item["来源"])}">{item["来源"]}</span>'
            f'<span class="time">{item["时间"]}</span>'
            f'</div>{title_block}{orig_block}</article>')

def render_section(sid, label, items, accent, bg):
    count = len(items)
    is_security = sid == "security"

    if not items:
        body = '<p class="empty">暂无相关新闻</p>'
    elif count <= PREVIEW_COUNT:
        body = "\n".join(render_card(i, is_security) for i in items)
    else:
        preview = "\n".join(render_card(i, is_security) for i in items[:PREVIEW_COUNT])
        rest    = "\n".join(render_card(i, is_security) for i in items[PREVIEW_COUNT:])
        body = (f'{preview}'
                f'<details class="more-block">'
                f'<summary class="more-btn">展开更多 {count - PREVIEW_COUNT} 条</summary>'
                f'<div class="more-inner">{rest}</div>'
                f'</details>')

    return (f'<section id="{sid}" style="border-top:4px solid {accent};background:{bg}">'
            f'<h2 class="sec-title" style="color:{accent}">'
            f'{label} <span class="sec-count">{count}</span></h2>'
            f'{body}'
            f'</section>')

def render_html(news_list):
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    classified = classify(news_list)

    nav_items = "".join(
        f'<a class="nav-item" href="#{sid}" style="--a:{accent}">{label}</a>'
        for sid, label, _, accent, _ in SECTIONS
    )
    sections_html = "\n".join(
        render_section(sid, label, classified[sid], accent, bg)
        for sid, label, _, accent, bg in SECTIONS
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Web3 News</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0f172a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="W3 新闻">
<link rel="apple-touch-icon" href="icon-192.png">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB",sans-serif;
  background:#f0f2f5;color:#1a1a2e;min-height:100vh;font-size:15px;
  -webkit-text-size-adjust:100%;text-size-adjust:100%}}
header{{background:#0f172a;color:#e2e8f0;padding:1.5rem 1.5rem .75rem}}
header h1{{font-size:1.5rem;font-weight:700;letter-spacing:.02em}}
header p{{margin-top:.4rem;font-size:.875rem;color:#94a3b8}}
nav{{position:sticky;top:0;z-index:100;background:#0f172a;
  border-top:1px solid #1e293b;padding:.5rem 1rem;
  display:flex;gap:.5rem;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}}
nav::-webkit-scrollbar{{display:none}}
.nav-item{{flex-shrink:0;font-size:.78rem;font-weight:600;color:#94a3b8;
  text-decoration:none;padding:.4rem .75rem;border-radius:99px;
  white-space:nowrap;transition:background .15s,color .15s}}
.nav-item:hover,.nav-item:active{{background:#1e293b;color:var(--a,#e2e8f0)}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:1rem;
  max-width:1600px;margin:1.25rem auto;padding:0 1rem;align-items:start}}
section{{border-radius:14px;padding:1.1rem 1.1rem}}
.sec-title{{font-size:1rem;font-weight:700;margin-bottom:.9rem;
  padding-bottom:.5rem;border-bottom:1px solid rgba(0,0,0,.07);
  display:flex;align-items:center;gap:.4rem}}
.sec-count{{font-size:.7rem;font-weight:600;background:rgba(0,0,0,.08);
  color:inherit;padding:.15rem .45rem;border-radius:99px}}
.empty{{font-size:.85rem;color:#94a3b8;padding:.5rem 0}}
.card{{background:#fff;border-radius:10px;padding:.85rem .95rem;
  margin-bottom:.7rem;box-shadow:0 1px 3px rgba(0,0,0,.07);
  transition:box-shadow .2s;-webkit-tap-highlight-color:transparent}}
.card:hover{{box-shadow:0 4px 14px rgba(0,0,0,.11)}}
.card-alert{{border-left:3px solid #ef4444;background:#fff8f8}}
.card-alert:hover{{box-shadow:0 4px 14px rgba(239,68,68,.12)}}
.meta{{display:flex;gap:.35rem;align-items:center;margin-bottom:.5rem;flex-wrap:wrap}}
.source{{font-size:.67rem;font-weight:700;padding:.18rem .5rem;
  border-radius:99px;white-space:nowrap}}
.time{{font-size:.72rem;color:#94a3b8}}
.title{{font-size:.92rem;font-weight:600;color:#1e293b;text-decoration:none;
  line-height:1.65;display:block;word-break:break-all}}
.title:hover{{color:#2563eb}}
.orig{{margin-top:.55rem;border-top:1px solid #f1f5f9;padding-top:.5rem}}
.orig summary{{font-size:.75rem;color:#64748b;cursor:pointer;user-select:none;
  list-style:none;display:flex;align-items:center;gap:.3rem;
  padding:.2rem 0;min-height:2rem}}
.orig summary::marker,.orig summary::-webkit-details-marker{{display:none}}
.orig summary::after{{content:"▾";font-size:.68rem;transition:transform .2s}}
.orig[open] summary::after{{transform:rotate(-180deg)}}
.orig-text{{margin-top:.35rem;font-size:.82rem;color:#64748b;
  line-height:1.55;word-break:break-word}}
.more-block{{margin-top:.7rem}}
.more-block summary::marker,.more-block summary::-webkit-details-marker{{display:none}}
.more-btn{{font-size:.78rem;font-weight:600;color:#64748b;cursor:pointer;
  user-select:none;list-style:none;display:inline-flex;align-items:center;gap:.3rem;
  padding:.4rem .8rem;border-radius:99px;background:rgba(0,0,0,.06);
  transition:background .15s;-webkit-tap-highlight-color:transparent}}
.more-btn:hover{{background:rgba(0,0,0,.1)}}
.more-block summary::after{{content:"▾";font-size:.68rem;transition:transform .2s;margin-left:.2rem}}
.more-block[open] summary::after{{transform:rotate(-180deg)}}
.more-inner{{margin-top:.7rem}}
footer{{text-align:center;padding:2rem 1rem;font-size:.8rem;color:#94a3b8;line-height:1.6}}
@media(max-width:1200px){{
  .grid{{grid-template-columns:repeat(3,1fr)}}
}}
@media(max-width:768px){{
  .grid{{grid-template-columns:repeat(2,1fr)}}
}}
@media(max-width:600px){{
  header{{padding:1.1rem 1rem .6rem}}
  header h1{{font-size:1.3rem}}
  .grid{{grid-template-columns:1fr;padding:0 .75rem;gap:.9rem;margin-top:1rem}}
  section{{padding:.9rem .9rem}}
  .card{{padding:.75rem .8rem}}
  .title{{font-size:.9rem}}
}}
</style>
</head>
<body>
<header>
  <h1>⚡ Web3 News</h1>
  <p>共 {len(news_list)} 条 · 更新于 {updated}</p>
</header>
<nav>
{nav_items}
</nav>
<div class="grid">
{sections_html}
</div>
<footer>由 web3-news-agent 自动生成</footer>
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

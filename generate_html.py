# -*- coding: utf-8 -*-
import json
from datetime import datetime

DATA_FILE = "news_data.json"
OUTPUT_FILE = "index.html"

# 各来源标签的配色（背景色, 文字色）
SOURCE_COLORS = {
    "TheBlock":      ("#dbeafe", "#1d4ed8"),   # 蓝
    "Cointelegraph": ("#fef3c7", "#b45309"),   # 橙
    "CoinDesk":      ("#d1fae5", "#065f46"),   # 绿
    "BlockBeats":    ("#ede9fe", "#6d28d9"),   # 紫
    "吴说区块链":    ("#fce7f3", "#9d174d"),   # 粉
    "PANews":        ("#ccfbf1", "#0f766e"),   # 青
}
DEFAULT_COLOR = ("#f1f5f9", "#475569")

def source_style(name):
    bg, fg = SOURCE_COLORS.get(name, DEFAULT_COLOR)
    return f'background:{bg};color:{fg}'

def load_news(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def render_card(item):
    zh   = item.get("title_zh", "")
    en   = item["标题"]
    link = item["链接"]
    # 有中文翻译：主标题用中文，可展开看英文原标题
    if zh:
        title_block = f'<a class="title" href="{link}" target="_blank" rel="noopener">{zh}</a>'
        orig_block  = (f'<details class="orig">'
                       f'<summary>英文原标题</summary>'
                       f'<p class="orig-text">{en}</p>'
                       f'</details>')
    else:
        title_block = f'<a class="title" href="{link}" target="_blank" rel="noopener">{en}</a>'
        orig_block  = ""

    return (f'<article class="card">'
            f'<div class="meta">'
            f'<span class="source" style="{source_style(item["来源"])}">{item["来源"]}</span>'
            f'<span class="time">{item["时间"]}</span>'
            f'</div>'
            f'{title_block}{orig_block}'
            f'</article>')

def render_html(news_list):
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = "\n".join(render_card(i) for i in news_list)

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
  background:#f0f2f5;color:#1a1a2e;min-height:100vh;font-size:16px;
  -webkit-text-size-adjust:100%;text-size-adjust:100%}}
header{{background:#0f172a;color:#e2e8f0;padding:1.8rem 1.5rem}}
header h1{{font-size:1.5rem;font-weight:700;letter-spacing:.02em}}
header p{{margin-top:.5rem;font-size:.875rem;color:#94a3b8;line-height:1.5}}
main{{max-width:780px;margin:1.5rem auto;padding:0 1rem}}
.card{{background:#fff;border-radius:14px;padding:1.2rem 1.4rem;
  margin-bottom:1rem;box-shadow:0 1px 4px rgba(0,0,0,.07);
  transition:box-shadow .2s;-webkit-tap-highlight-color:transparent}}
.card:hover{{box-shadow:0 5px 18px rgba(0,0,0,.12)}}
.meta{{display:flex;gap:.5rem;align-items:center;margin-bottom:.75rem;flex-wrap:wrap}}
.source{{font-size:.72rem;font-weight:700;padding:.25rem .65rem;
  border-radius:99px;white-space:nowrap;letter-spacing:.01em}}
.time{{font-size:.8rem;color:#94a3b8}}
.title{{font-size:1.08rem;font-weight:600;color:#1e293b;text-decoration:none;
  line-height:1.7;display:block;word-break:break-all}}
.title:hover{{color:#2563eb}}
.orig{{margin-top:.75rem;border-top:1px solid #f1f5f9;padding-top:.65rem}}
.orig summary{{font-size:.82rem;color:#64748b;cursor:pointer;user-select:none;
  list-style:none;display:flex;align-items:center;gap:.35rem;
  padding:.3rem 0;min-height:2.5rem}}
.orig summary::marker,.orig summary::-webkit-details-marker{{display:none}}
.orig summary::after{{content:"▾";font-size:.75rem;transition:transform .2s;margin-left:.1rem}}
.orig[open] summary::after{{transform:rotate(-180deg)}}
.orig-text{{margin-top:.5rem;font-size:.9rem;color:#64748b;
  line-height:1.65;word-break:break-word}}
footer{{text-align:center;padding:2.5rem 1rem;font-size:.8rem;color:#94a3b8;line-height:1.6}}
@media(max-width:600px){{
  body{{font-size:16px}}
  header{{padding:1.25rem 1rem}}
  header h1{{font-size:1.35rem}}
  main{{padding:0 .75rem;margin-top:1rem}}
  .card{{padding:1rem 1.1rem;border-radius:12px;margin-bottom:.85rem}}
  .title{{font-size:1.05rem;line-height:1.72}}
  .meta{{margin-bottom:.65rem}}
  .orig{{margin-top:.65rem;padding-top:.6rem}}
  .orig summary{{min-height:2.75rem;font-size:.85rem}}
}}
</style>
</head>
<body>
<header>
  <h1>⚡ Web3 News</h1>
  <p>共 {len(news_list)} 条 · 更新于 {updated}</p>
</header>
<main>
{cards}
</main>
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

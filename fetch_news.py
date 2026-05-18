# -*- coding: utf-8 -*-
import os, certifi
os.environ["SSL_CERT_FILE"] = certifi.where()  # 修复 macOS Python 3 SSL 证书缺失问题

import feedparser
from datetime import datetime

# RSS 源列表：英文 + 中文 Web3 媒体
RSS_FEEDS = {
    "TheBlock":      "https://www.theblock.co/rss.xml",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "BlockBeats":    "https://www.theblockbeats.info/rss",
    "吴说区块链":    "https://wublock.substack.com/feed",
    "PANews":        "https://www.panewslab.com/rss",
}

def parse_time(entry):
    # 优先使用 published_parsed，回退到当前时间
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
    return "未知时间"

def fetch_news(limit=5):
    all_news = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_news.append({
                "来源": source,
                "标题": entry.get("title", "无标题"),
                "链接": entry.get("link", ""),
                "时间": parse_time(entry),
            })

    # 按时间降序排列，取前 N 条
    all_news.sort(key=lambda x: x["时间"], reverse=True)
    return all_news[:limit]

def print_news(news_list):
    print("=" * 60)
    for i, item in enumerate(news_list, 1):
        print("[{}] {}  {}".format(i, item["来源"], item["时间"]))
        print(u"    标题：{}".format(item["标题"]))
        print(u"    链接：{}".format(item["链接"]))
        print("-" * 60)

if __name__ == "__main__":
    news = fetch_news(limit=5)
    print_news(news)

# -*- coding: utf-8 -*-
import json
import os
from fetch_news import fetch_news

DATA_FILE = "news_data.json"

def load_existing(filepath):
    """从 JSON 文件加载已有新闻，返回列表和标题集合"""
    if not os.path.exists(filepath):
        return [], set()
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    titles = {item["标题"] for item in data}
    return data, titles

def save_news(filepath, news_list):
    """将新闻列表写回 JSON 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

def dedupe_and_save(limit=50):
    existing, seen_titles = load_existing(DATA_FILE)
    fresh = fetch_news(limit=limit)

    added, skipped = [], 0
    for item in fresh:
        if item["标题"] in seen_titles:
            skipped += 1
        else:
            added.append(item)
            seen_titles.add(item["标题"])

    save_news(DATA_FILE, added + existing)
    print(f"新增了 {len(added)} 条，跳过了 {skipped} 条重复")

if __name__ == "__main__":
    dedupe_and_save()

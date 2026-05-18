# -*- coding: utf-8 -*-
import json
import re
from deep_translator import GoogleTranslator

DATA_FILE = "news_data.json"

def is_chinese(text):
    """判断标题是否已含中文，是则无需翻译"""
    return bool(re.search(r'[一-鿿]', text))

def translate_news():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        news = json.load(f)

    translator = GoogleTranslator(source="auto", target="zh-CN")
    updated = 0

    for item in news:
        # 已有翻译、或标题本身是中文，则跳过
        if item.get("title_zh") or is_chinese(item["标题"]):
            item.setdefault("title_zh", item["标题"])  # 中文标题直接复用
            continue
        try:
            item["title_zh"] = translator.translate(item["标题"])
            updated += 1
            print(f"  ✓ {item['title_zh']}")
        except Exception as e:
            print(f"  ✗ 翻译失败：{item['标题'][:40]}… ({e})")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

    print(f"\n共翻译 {updated} 条，已保存到 {DATA_FILE}")

if __name__ == "__main__":
    translate_news()

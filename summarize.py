# -*- coding: utf-8 -*-
import json
import anthropic
from dotenv import load_dotenv

# 自动从 .env 文件加载 ANTHROPIC_API_KEY
load_dotenv()

DATA_FILE = "news_data.json"
OUTPUT_FILE = "summary.md"

def load_latest_news(filepath, limit=10):
    """读取最新的 N 条新闻"""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[:limit]

def format_news_for_prompt(news_list):
    """将新闻列表格式化为提示词文本"""
    lines = []
    for i, item in enumerate(news_list, 1):
        lines.append(f"{i}. [{item['来源']}] {item['时间']}")
        lines.append(f"   标题：{item['标题']}")
        lines.append(f"   链接：{item['链接']}")
    return "\n".join(lines)

def generate_summary(news_text):
    """调用 Claude API 生成中文摘要（流式输出）"""
    client = anthropic.Anthropic()

    prompt = f"""以下是最新的 Web3 / 加密货币新闻，请用中文写一段简洁易读的摘要：
- 归纳主要热点与趋势
- 每条新闻用一两句话概括
- 结尾给出整体市场简评

新闻列表：
{news_text}
"""

    # 使用流式调用，避免长输出超时
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        result = stream.get_final_message()

    return result.content[0].text

def save_summary(filepath, summary, news_list):
    """将摘要写入 Markdown 文件"""
    from datetime import datetime
    header = f"# Web3 新闻摘要\n\n_生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + summary + "\n")

def main():
    news = load_latest_news(DATA_FILE)
    print(f"已读取 {len(news)} 条新闻，正在生成摘要...")

    news_text = format_news_for_prompt(news)
    summary = generate_summary(news_text)

    save_summary(OUTPUT_FILE, summary, news)
    print(f"摘要已保存至 {OUTPUT_FILE}")
    print("\n" + "=" * 50)
    print(summary)

if __name__ == "__main__":
    main()

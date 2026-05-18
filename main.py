# -*- coding: utf-8 -*-
import schedule
import time
from datetime import datetime, timedelta

from dedupe import dedupe_and_save
from translate_news import translate_news
from generate_html import main as generate_html

def run_pipeline():
    now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    next_run = (datetime.now() + timedelta(minutes=30)).strftime("%H:%M")
    print(f"\n{'─'*45}")
    print(f"[{now}] 正在更新新闻...")
    try:
        dedupe_and_save()
        translate_news()
        generate_html()
        print(f"✓ 更新完成，下次更新：{next_run}")
    except Exception as e:
        print(f"✗ 更新失败：{e}")

# 启动时立即运行一次
run_pipeline()

# 此后每 30 分钟自动执行
schedule.every(30).minutes.do(run_pipeline)
print("\n定时任务已启动，每 30 分钟自动更新（Ctrl+C 退出）")

while True:
    schedule.run_pending()
    time.sleep(1)

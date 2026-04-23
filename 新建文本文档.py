import os
import requests
from datetime import datetime

# 这里演示使用一个公开的 News API（你可以去 newsapi.org 免费申请一个 Key）
NEWS_API_KEY = "YOUR_NEWS_API_KEY" 
URL = f"https://newsapi.org/v2/top-headlines?country=cn&category=business&apiKey={NEWS_API_KEY}"

def get_news():
    # 模拟抓取或调用 API
    # 在实际操作中，这里会接入 AI 大模型进行筛选
    response = requests.get(URL)
    articles = response.json().get('articles', [])[:10] # 取前10条
    return articles

def generate_html(news_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 这里定义网页的头部和样式（与之前给你的 HTML 一致）
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>今日有影响力新闻</title>
        <style>
            body {{ font-family: sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 10px; }}
            .item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
            .tag {{ font-size: 0.8em; color: #2c3e50; background: #eee; padding: 2px 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>今日 10 条影响力新闻</h1>
            <p>最后更新时间：{now}</p>
    """
    
    for idx, item in enumerate(news_list):
        title = item.get('title', '无标题')
        desc = item.get('description', '点击查看详情')
        link = item.get('url', '#')
        html_template += f"""
            <div class="item">
                <h3>{idx+1}. <a href="{link}">{title}</a></h3>
                <p>{desc}</p>
            </div>
        """
        
    html_template += """
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    news = get_news()
    generate_html(news)
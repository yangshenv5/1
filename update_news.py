import requests
from datetime import datetime
import xml.etree.ElementTree as ET

def get_news():
    # 使用财联社或类似高价值财经 RSS（这里以一个稳定的财经源为例）
    rss_url = "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best"
    news_list = []
    try:
        response = requests.get(rss_url, timeout=10)
        root = ET.fromstring(response.content)
        for item in root.findall('.//item')[:10]:
            news_list.append({
                'title': item.find('title').text,
                'description': "点击查看深度报道及市场影响分析。",
                'url': item.find('link').text
            })
    except Exception as e:
        # 如果抓取失败，显示一组备用重要讯息
        news_list = [{'title': '全球市场观察：关注央行最新利率决议', 'description': '市场普遍预期将维持现行政策，重点关注会后声明。', 'url': '#'}]
    return news_list

def generate_html(news_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>今日 10 条影响力新闻</title>
        <style>
            body {{ font-family: 'PingFang SC', sans-serif; background: #f0f2f5; padding: 40px 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a1a1a; border-left: 5px solid #2c3e50; padding-left: 15px; }}
            .time {{ color: #888; margin-bottom: 30px; }}
            .item {{ border-bottom: 1px solid #eee; padding: 20px 0; }}
            .item:last-child {{ border: none; }}
            .item a {{ color: #1a1a1a; text-decoration: none; font-size: 1.2em; font-weight: bold; }}
            .item a:hover {{ color: #3498db; }}
            .desc {{ color: #666; margin-top: 10px; font-size: 0.95em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>今日 10 条影响力新闻</h1>
            <p class="time">最后更新时间：{now} (北京时间)</p>
    """
    for item in news_list:
        html_template += f"""
            <div class="item">
                <a href="{item['url']}" target="_blank">{item['title']}</a>
                <div class="desc">{item['description']}</div>
            </div>
        """
    html_template += "</div></body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    news = get_news()
    generate_html(news)

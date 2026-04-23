import requests
import re
from datetime import datetime

def get_news():
    # 改用新浪财经的实时新闻接口，更适合国内用户
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&k=&num=10&page=1"
    news_list = []
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        items = data.get('result', {}).get('data', [])
        
        for item in items:
            news_list.append({
                'title': item.get('title'),
                'description': item.get('summary') if item.get('summary') else "点击查看财经详情。",
                'url': item.get('url')
            })
    except Exception as e:
        print(f"抓取失败: {e}")
        # 紧急备用内容
        news_list = [{
            'title': '正在获取实时财经数据，请稍后刷新',
            'description': '如果持续看到此信息，请检查 API 接口连接。',
            'url': 'https://finance.sina.com.cn/'
        }]
    
    # 如果接口返回空，手动塞入一条提示
    if not news_list:
        news_list = [{'title': '今日暂无重大更新', 'description': '请关注稍后的市场开盘动态。', 'url': '#'}]
        
    return news_list

def generate_html(news_list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>今日 10 条影响力新闻</title>
        <style>
            body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f4f7f9; margin: 0; padding: 20px; }}
            .container {{ max-width: 700px; margin: 20px auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            h1 {{ color: #2c3e50; font-size: 24px; text-align: center; margin-bottom: 5px; }}
            .time {{ color: #95a5a6; text-align: center; font-size: 14px; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
            .item {{ padding: 15px 0; border-bottom: 1px dashed #eee; }}
            .item:last-child {{ border: none; }}
            .item a {{ color: #2980b9; text-decoration: none; font-size: 18px; font-weight: bold; line-height: 1.4; }}
            .item a:hover {{ color: #c0392b; text-decoration: underline; }}
            .desc {{ color: #7f8c8d; margin-top: 8px; font-size: 14px; line-height: 1.6; }}
            footer {{ text-align: center; margin-top: 20px; color: #bdc3c7; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>今日 10 条影响力新闻</h1>
            <p class="time">更新于：{now} (北京时间)</p>
    """
    for item in news_list:
        html_template += f"""
            <div class="item">
                <a href="{item['url']}" target="_blank">{item['title']}</a>
                <div class="desc">{item['description']}</div>
            </div>
        """
    html_template += """
            <footer>© 个人投资日报自动化系统</footer>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    news = get_news()
    generate_html(news)

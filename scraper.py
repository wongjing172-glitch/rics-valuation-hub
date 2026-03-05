import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_hk_news():
    # 抓取香港地產新聞 (以 HKET 住宅版為例)
    url = "https://ps.hket.com/s/住宅"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = []
        
        # 關鍵字過濾
        keywords = ["華富", "安達", "北部都會區", "新田", "重建", "地契", "估值"]
        
        # 抓取新聞標題與連結
        for article in soup.select('.title-link'):
            title = article.text.strip()
            link = "https://ps.hket.com" + article['href']
            
            match = next((k for k in keywords if k in title), None)
            
            if match:
                news_items.append({
                    "title": title,
                    "url": link,
                    "tag": match,
                    "date": datetime.date.today().strftime("%Y-%m-%d")
                })
        
        return news_items[:10]
    except Exception as e:
        print(f"抓取失敗: {e}")
        return []

if __name__ == "__main__":
    data = scrape_hk_news()
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("成功更新新聞數據！")

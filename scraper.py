import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_hk_news():
    # 擴大搜尋範圍，同時抓取住宅和土地新聞
    urls = [
        "https://ps.hket.com/s/住宅",
        "https://ps.hket.com/s/土地地契"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    news_items = []
    # 增加更多備考相關關鍵字
    keywords = ["華富", "安達", "北部都會區", "新田", "重建", "地契", "估值", "樓市", "住宅", "地標", "招標"]
    
    for url in urls:
        try:
            print(f"正在抓取: {url}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 修改抓取邏輯，確保能抓到標題
            articles = soup.find_all(['a', 'h3'], class_=['title-link', 'title'])
            
            for article in articles:
                title = article.get_text().strip()
                link = article.get('href', '')
                
                if not link.startswith('http'):
                    link = "https://ps.hket.com" + link
                
                # 關鍵字檢查
                match = next((k for k in keywords if k in title), None)
                
                if match and len(title) > 5: # 確保標題完整
                    news_items.append({
                        "title": title,
                        "url": link,
                        "tag": match,
                        "date": datetime.date.today().strftime("%Y-%m-%d")
                    })
        except Exception as e:
            print(f"抓取 {url} 失敗: {e}")
            
    # 去除重複的新聞
    unique_news = {v['url']: v for v in news_items}.values()
    return list(unique_news)[:15]

if __name__ == "__main__":
    data = scrape_hk_news()
    if not data:
        # 如果真的沒抓到，給一個保底數據，讓網頁不至於空白
        data = [{
            "title": "目前暫無即時特定新聞，請查看研究專案",
            "url": "#",
            "tag": "系統提示",
            "date": datetime.date.today().strftime("%Y-%m-%d")
        }]
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"成功更新 {len(data)} 條新聞數據！")

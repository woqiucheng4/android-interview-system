import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.database import insert_raw_content

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

KEYWORDS = ["Android 面试", "Android 高频", "Android 真题"]

def search_juejin(keyword):
    print(f"Searching Juejin for: {keyword}")
    url = "https://api.juejin.cn/search_api/v1/search"
    payload = {
        "key_word": keyword,
        "id_type": 2, # Articles
        "limit": 5,
        "cursor": "0",
        "search_type": 0
    }
    
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data", [])
        return []
    except Exception as e:
        print(f"Juejin search error: {e}")
        return []

def get_article_content(article_id):
    url = f"https://juejin.cn/post/{article_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Juejin article content is usually in a simpler container for SEO
            # But the main content is often in class="markdown-body"
            content_div = soup.find('div', class_='markdown-body')
            if content_div:
                return content_div.get_text('\n')
            
            # Fallback: try to find the script tag that has server side data if main body is empty
            # (Simplification: just return None if standard scraping fails)
    except Exception as e:
        print(f"Juejin fetch content error: {e}")
    return None

def run_juejin_crawler():
    print("Starting Juejin Crawler...")
    for keyword in KEYWORDS:
        items = search_juejin(keyword)
        for item in items:
            result_model = item.get("result_model", {})
            article_id = result_model.get("article_id")
            title = result_model.get("article_info", {}).get("title")
            url = f"https://juejin.cn/post/{article_id}"
            
            if not article_id or not title:
                continue
                
            print(f"Processing: {title}")
            content = get_article_content(article_id)
            
            if content:
                # Store
                title_fmt = f"[Juejin] {title}"
                insert_raw_content(title_fmt, content, "juejin", url)
                print(f"Saved {title}")
            
            time.sleep(2)

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    run_juejin_crawler()

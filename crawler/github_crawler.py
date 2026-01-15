import requests
import base64
import time
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.database import insert_raw_content

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Optional: for higher rate limits
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "AndroidInterviewBot/1.0"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

KEYWORDS = ["Android 面试", "Android interview", "Android 高频"]

def search_repositories(keyword):
    print(f"Searching GitHub for: {keyword}")
    url = "https://api.github.com/search/repositories"
    params = {
        "q": keyword,
        "sort": "stars",
        "order": "desc",
        "per_page": 5 # Limit to top 5 to avoid spam
    }
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        return resp.json().get("items", [])
    except Exception as e:
        print(f"GitHub search failed: {e}")
        return []

def get_readme_content(owner, repo, default_branch):
    # Try different common readme filenames
    for filename in ["README.md", "readme.md", "README.MD"]:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/{filename}"
        try:
            resp = requests.get(url, headers=HEADERS)
            if resp.status_code == 200:
                return resp.text
        except:
            continue
    return None

def run_github_crawler():
    print("Starting GitHub Crawler...")
    for keyword in KEYWORDS:
        repos = search_repositories(keyword)
        for repo in repos:
            name = repo["name"]
            full_name = repo["full_name"]
            url = repo["html_url"]
            desc = repo["description"] or ""
            default_branch = repo["default_branch"]
            
            print(f"Processing: {full_name}")
            
            content = get_readme_content(full_name.split('/')[0], name, default_branch)
            
            if content:
                # Store in DB
                # Title combines repo name and description
                title = f"[GitHub] {full_name}: {desc[:50]}"
                insert_raw_content(title, content, "github", url)
                print(f"Saved {full_name}")
            
            time.sleep(1) # Respect rate limits

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    run_github_crawler()

import os
import sys

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.database import init_db
from crawler.github_crawler import run_github_crawler
from crawler.juejin_crawler import run_juejin_crawler
from ai.processor import process_content
from ai.processor import process_content
from utils.email_sender import send_daily_report

def main():
    print("=== Android Interview System: Daily Sync Started ===")
    
    # 1. Initialize DB
    print("\n[Step 1] Initializing Database...")
    init_db()
    
    # 2. Run Crawlers
    print("\n[Step 2] Running GitHub Crawler...")
    try:
        run_github_crawler()
    except Exception as e:
        print(f"GitHub Crawler failed: {e}")

    print("\n[Step 3] Running Juejin Crawler...")
    try:
        run_juejin_crawler()
    except Exception as e:
        print(f"Juejin Crawler failed: {e}")
        
    # 3. Process with AI
    print("\n[Step 4] Running AI Processor...")
    new_questions = []
    try:
        new_questions = process_content()
    except Exception as e:
        print(f"AI Processor failed: {e}")
        
    # 4. Email Report
    print("\n[Step 5] Sending Email Report...")
    try:
        if new_questions:
            send_daily_report(new_questions)
        else:
            print("No new questions to report.")
    except Exception as e:
        print(f"Email Sender failed: {e}")
        
    print("\n=== Daily Sync Completed ===")

if __name__ == "__main__":
    main()

import requests
import os
import json

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

def call_qwen_api(system_prompt, user_message):
    if not DASHSCOPE_API_KEY:
        print("Error: DASHSCOPE_API_KEY not found.")
        return None
        
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-plus",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5,
        "response_format": {"type": "json_object"} 
    }
    
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API Error {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

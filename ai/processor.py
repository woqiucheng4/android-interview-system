import json
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db.database import get_unprocessed_content, mark_processed, insert_question, init_db
from ai.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from ai.dashscope_client import call_qwen_api

def process_content():
    print("Starting AI Processor...")
    # Fetch pending content
    rows = get_unprocessed_content(limit=5)
    
    if not rows:
        print("No new content to process.")
        return

    new_questions = []

    for row in rows:
        row_id = row['id']
        title = row['title']
        content = row['content']
        source = row['source']
        
        print(f"Processing ID {row_id}: {title}...")
        
        # Truncate content to avoid exceeding token limits (rough est)
        # Keep first 6000 chars which usually contains the core info
        truncated_content = content[:6000]
        
        user_msg = USER_PROMPT_TEMPLATE.format(title=title, content=truncated_content)
        
        ai_response = call_qwen_api(SYSTEM_PROMPT, user_msg)
        
        if ai_response:
            try:
                # Clean up if AI output markdown code blocks
                clean_json = ai_response.replace("```json", "").replace("```", "").strip()
                questions = json.loads(clean_json)
                
                if isinstance(questions, list):
                    for q in questions:
                        q_data = {
                            "raw_id": row_id,
                            "question": q.get("question", "Unknown"),
                            "answer": q.get("standard_answer", "No answer provided"),
                            "follow_up": json.dumps(q.get("follow_up_questions", []), ensure_ascii=False),
                            "category": q.get("category", "General"),
                            "level": q.get("level", "Middle"),
                            "is_vip": False,
                            "source": source
                        }
                        insert_question(**q_data)
                        new_questions.append(q_data)
                        
                    print(f"  -> Extracted {len(questions)} questions.")
                    mark_processed(row_id)
                else:
                    print("  -> AI returned valid JSON but not a list.")
            except json.JSONDecodeError:
                print("  -> Failed to parse AI JSON response.")
                print(ai_response[:100])
            except Exception as e:
                print(f"  -> Error saving questions: {e}")
        else:
            print("  -> AI request failed.")
            
    return new_questions

if __name__ == "__main__":
    init_db()
    process_content()

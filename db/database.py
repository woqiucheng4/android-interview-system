import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'interview.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    conn = get_conn()
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.close()

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_raw_content(title, content, source, url):
    conn = get_conn()
    try:
        conn.execute('''
            INSERT OR IGNORE INTO raw_content (title, content, source, url, create_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, source, url, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error inserting raw content: {e}")
    finally:
        conn.close()

def get_unprocessed_content(limit=5):
    conn = get_conn()
    rows = conn.execute('SELECT * FROM raw_content WHERE is_processed = 0 LIMIT ?', (limit,)).fetchall()
    conn.close()
    return rows

def mark_processed(raw_id):
    conn = get_conn()
    conn.execute('UPDATE raw_content SET is_processed = 1 WHERE id = ?', (raw_id,))
    conn.commit()
    conn.close()

def insert_question(raw_id, question, answer, follow_up, category, level, is_vip, source):
    conn = get_conn()
    try:
        conn.execute('''
            INSERT INTO question_bank 
            (raw_id, question, answer, follow_up, category, level, is_vip, source, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (raw_id, question, answer, follow_up, category, level, is_vip, source, datetime.now()))
        conn.commit()
    except Exception as e:
        print(f"Error inserting question: {e}")
    finally:
        conn.close()

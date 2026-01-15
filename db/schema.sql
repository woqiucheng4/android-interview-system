CREATE TABLE IF NOT EXISTS raw_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS question_bank (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_id INTEGER,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    follow_up TEXT,
    category TEXT,
    level TEXT,
    is_vip BOOLEAN DEFAULT 0,
    source TEXT,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(raw_id) REFERENCES raw_content(id)
);

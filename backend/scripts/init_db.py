import sqlite3
import json
from data.personality_questions import get_all_questions

def init_database():
    # 建立資料庫連線
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()

    # 刪除舊表（如果存在）
    cursor.execute("DROP TABLE IF EXISTS test_session")
    cursor.execute("DROP TABLE IF EXISTS test_answer")
    cursor.execute("DROP TABLE IF EXISTS test_question")
    cursor.execute("DROP TABLE IF EXISTS test_report")

    # 建立 test_question 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category VARCHAR(32) NOT NULL,
            test_type VARCHAR(16) NOT NULL,
            options TEXT NOT NULL,
            weight TEXT NOT NULL
        )
    ''')

    # 建立 test_answer 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(64) NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            session_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES test_question (id)
        )
    ''')

    # 建立 test_session 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_session (
            id INTEGER PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL,
            test_type VARCHAR(16) NOT NULL,
            question_ids TEXT NOT NULL,
            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            finished_at DATETIME,
            paused_at DATETIME,
            total_time_seconds INTEGER DEFAULT 0,
            status VARCHAR(16) DEFAULT 'in_progress'
        )
    ''')

    # 建立 test_report 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(64) NOT NULL,
            test_type VARCHAR(16) NOT NULL,
            result TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 匯入題庫資料
    questions = get_all_questions()
    
    # 先清空現有數據
    cursor.execute("DELETE FROM test_question")
    
    for question in questions:
        cursor.execute(
            '''
            INSERT INTO test_question (id, text, category, test_type, options, weight)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                getattr(question, 'id', None),
                question.text,
                question.category,
                question.test_type,
                json.dumps(question.options),
                json.dumps(question.weight)
            )
        )

    # 提交變更並關閉連線
    conn.commit()
    conn.close()

    print(f"資料庫初始化完成！已匯入 {len(questions)} 題題庫資料。")

if __name__ == "__main__":
    init_database() 
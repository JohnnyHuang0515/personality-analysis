import sqlite3
import json
from data.personality_questions import get_all_questions

def init_database():
    # 建立資料庫連線
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()

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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES test_question (id)
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
    for question in questions:
        cursor.execute(
            '''
            INSERT OR IGNORE INTO test_question (id, text, category, test_type, options, weight)
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
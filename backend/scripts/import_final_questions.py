import sqlite3
import sys
import os
import json

# 確保可以匯入 personality_questions.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.personality_questions import get_all_questions

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'personality_test.db')

def import_final_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 確保 test_question 表存在
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category VARCHAR(32) NOT NULL,
            test_type VARCHAR(16) NOT NULL,
            options TEXT NOT NULL,
            weight TEXT NOT NULL,
            is_reverse BOOLEAN DEFAULT FALSE
        )
    ''')

    # 清空舊資料
    cursor.execute('DELETE FROM test_question')

    questions = get_all_questions()
    for q in questions:
        cursor.execute(
            '''
            INSERT INTO test_question (text, category, test_type, options, weight, is_reverse)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                q.text,
                q.category,
                q.test_type,
                json.dumps(q.options, ensure_ascii=False),
                json.dumps(q.weight, ensure_ascii=False),
                int(q.is_reverse)
            )
        )
    conn.commit()
    print(f"已匯入 {len(questions)} 題 final 題庫！")
    conn.close()

if __name__ == "__main__":
    import_final_questions() 
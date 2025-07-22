import sqlite3
import json
import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_questions_from_json(file_path):
    """從 JSON 檔案載入題目"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
            weight TEXT NOT NULL,
            is_reverse BOOLEAN DEFAULT FALSE
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

    # 先清空現有數據
    cursor.execute("DELETE FROM test_question")
    
    # 載入各測驗類型的題目
    json_files = [
        ('data/BIG5_questions.json', 'BIG5'),
        ('data/DISC_questions.json', 'DISC'),
        ('data/enneagram_questions.json', 'enneagram'),
        ('data/MBTI_questions.json', 'MBTI')
    ]
    
    total_questions = 0
    
    for json_file, test_type in json_files:
        try:
            questions = load_questions_from_json(json_file)
            print(f"載入 {test_type} 題目: {len(questions)} 題")
            
            for question in questions:
                cursor.execute(
                    '''
                    INSERT INTO test_question (text, category, test_type, options, weight, is_reverse)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        question['text'],
                        question['category'],
                        question['test_type'],
                        json.dumps(question['options']),
                        json.dumps(question['weight']),
                        question.get('is_reverse', False)
                    )
                )
                total_questions += 1
                
        except Exception as e:
            print(f"載入 {json_file} 時發生錯誤: {e}")

    # 提交變更並關閉連線
    conn.commit()
    conn.close()
    
    print(f"資料庫初始化完成！已匯入 {total_questions} 題題庫資料。")

if __name__ == "__main__":
    init_database() 
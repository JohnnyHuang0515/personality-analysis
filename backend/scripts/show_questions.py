import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'personality_test.db')

def show_questions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT COUNT(*) FROM test_question')
        count = c.fetchone()[0]
        print(f'題目數量: {count}')
        if count > 0:
            c.execute('SELECT id, text, category, test_type FROM test_question LIMIT 5')
            print('\n前 5 筆題目：')
            for row in c.fetchall():
                print(row)
    except Exception as e:
        print('查詢失敗:', e)
    finally:
        conn.close()

if __name__ == '__main__':
    show_questions() 
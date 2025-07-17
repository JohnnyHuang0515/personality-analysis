import sqlite3
import json

def test_db_connection():
    try:
        # 連線到資料庫
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 查詢題庫數量
        cursor.execute("SELECT COUNT(*) FROM test_question")
        total_questions = cursor.fetchone()[0]
        
        # 查詢各類型題目數量
        cursor.execute("SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type")
        type_counts = cursor.fetchall()
        
        print("資料庫連線成功！")
        print(f"總題目數：{total_questions}")
        print("各類型題目數量：")
        for test_type, count in type_counts:
            print(f"  {test_type}: {count} 題")
        
        # 查詢前 3 題作為範例
        cursor.execute("SELECT id, text, test_type FROM test_question LIMIT 3")
        sample_questions = cursor.fetchall()
        
        print("範例題目：")
        for q_id, text, test_type in sample_questions:
            print(f"ID: {q_id}, 類型: {test_type}")
            print(f"題目: {text[:50]}...")
            print()
        
        conn.close()
        return True
    except Exception as e:
        print(f"資料庫連線失敗：{e}")
        return False

if __name__ == "__main__":
    test_db_connection() 
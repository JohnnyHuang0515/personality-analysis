import sqlite3
import json
import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.personality_questions import get_all_questions

def create_test_data():
    """創建完整的測試資料"""
    print("=== 創建完整測試資料 ===")
    
    # 載入所有題目
    questions = get_all_questions()
    
    # 連接資料庫
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 創建測試用戶
    test_user_id = "test_user_complete"
    
    # 清除舊的測試資料
    cursor.execute("DELETE FROM test_answer WHERE user_id = ?", (test_user_id,))
    
    # 為每個題目創建答案
    for question in questions:
        # 隨機選擇一個選項作為答案
        import random
        answer = random.choice(question.options)
        
        cursor.execute("""
            INSERT INTO test_answer (user_id, question_id, answer)
            VALUES (?, ?, ?)
        """, (test_user_id, question.id, answer))
    
    conn.commit()
    conn.close()
    
    print(f"已為用戶 {test_user_id} 創建 {len(questions)} 個答案")
    print("測試資料創建完成！")

if __name__ == "__main__":
    create_test_data() 
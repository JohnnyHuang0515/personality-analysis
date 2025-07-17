import sqlite3
import json

def fix_disc_options():
    """修正 DISC 題目 ID 98 的選項，從3個增加到4個"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("修正 DISC 題目選項...")
    
    # 查詢 ID 98 的題目
    cursor.execute("""
        SELECT id, text, options, weight 
        FROM test_question 
        WHERE id = 98
    """)
    
    question = cursor.fetchone()
    
    if not question:
        print("❌ 找不到 ID 98 的題目")
        conn.close()
        return
    
    question_id, text, options_json, weight_json = question
    
    print(f"題目 ID: {question_id}")
    print(f"題目: {text}")
    print(f"原始選項: {options_json}")
    
    # 修正選項，從3個增加到4個
    # 原始選項: ['快速上手', '互動學習', '按部就班']
    # 新增一個選項: '深入研究'
    fixed_options = ['快速上手', '互動學習', '按部就班', '深入研究']
    
    # 修正權重，確保每個選項都有對應的權重
    # DISC 權重通常是 D, I, S, C
    fixed_weight = {
        "D": 3,  # 快速上手 - 主導型
        "I": 2,  # 互動學習 - 影響型  
        "S": 1,  # 按部就班 - 穩定型
        "C": 0   # 深入研究 - 謹慎型
    }
    
    # 更新資料庫
    cursor.execute("""
        UPDATE test_question 
        SET options = ?, weight = ?
        WHERE id = ?
    """, (
        json.dumps(fixed_options),
        json.dumps(fixed_weight),
        question_id
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 修正完成")
    print(f"新選項: {fixed_options}")
    print(f"新權重: {fixed_weight}")

if __name__ == "__main__":
    fix_disc_options() 
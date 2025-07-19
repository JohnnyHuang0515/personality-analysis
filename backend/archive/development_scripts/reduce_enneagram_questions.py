import sqlite3
import json

def reduce_enneagram_questions():
    """刪除多餘的九型人格題目，只保留50題"""
    
    # 選中的題目ID列表（從優化腳本的結果）
    selected_ids = [
        151, 160, 169, 178, 187, 196,  # 類型1
        161, 179, 152,                  # 類型2
        153, 162, 189, 171,            # 類型3
        154, 163, 172, 181, 190,       # 類型4
        155, 173, 182, 191, 164,       # 類型5
        156, 165, 174, 201, 183, 192,  # 類型6
        166, 184, 193, 202,            # 類型7
        158, 185, 194, 167, 176,       # 類型8
        159, 168, 186, 204,            # 類型9
        278                             # 類型9 (單獨的)
    ]
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("縮減九型人格題目...")
    
    # 查詢所有九型人格題目
    cursor.execute("""
        SELECT id, text 
        FROM test_question 
        WHERE test_type = 'Enneagram' 
        ORDER BY id
    """)
    
    all_enneagram = cursor.fetchall()
    print(f"原始九型人格題目數: {len(all_enneagram)}")
    
    # 找出要刪除的題目
    to_delete = []
    to_keep = []
    
    for question_id, text in all_enneagram:
        if question_id in selected_ids:
            to_keep.append(question_id)
        else:
            to_delete.append(question_id)
    
    print(f"要保留的題目數: {len(to_keep)}")
    print(f"要刪除的題目數: {len(to_delete)}")
    
    # 確認要刪除的題目
    print(f"\n要刪除的題目:")
    for i, qid in enumerate(to_delete, 1):
        cursor.execute("SELECT text FROM test_question WHERE id = ?", (qid,))
        text = cursor.fetchone()[0]
        print(f"  {i:2d}. ID {qid}: {text[:50]}...")
    
    # 執行刪除
    if to_delete:
        placeholders = ','.join(['?' for _ in to_delete])
        cursor.execute(f"""
            DELETE FROM test_question 
            WHERE id IN ({placeholders})
        """, to_delete)
        
        conn.commit()
        print(f"\n✅ 成功刪除 {len(to_delete)} 題九型人格題目")
    else:
        print(f"\n✅ 沒有需要刪除的題目")
    
    # 確認最終結果
    cursor.execute("""
        SELECT COUNT(*) 
        FROM test_question 
        WHERE test_type = 'Enneagram'
    """)
    
    final_count = cursor.fetchone()[0]
    print(f"最終九型人格題目數: {final_count}")
    
    # 按類型統計
    cursor.execute("""
        SELECT category, COUNT(*) 
        FROM test_question 
        WHERE test_type = 'Enneagram' 
        GROUP BY category 
        ORDER BY category
    """)
    
    type_counts = cursor.fetchall()
    print(f"\n最終各類型題目數:")
    for type_name, count in type_counts:
        print(f"  {type_name}: {count} 題")
    
    conn.close()

if __name__ == "__main__":
    reduce_enneagram_questions() 
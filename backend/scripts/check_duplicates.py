import sqlite3
import json

def check_and_remove_duplicates():
    """檢查並刪除資料庫中重複的題目"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("檢查重複題目...")
    
    # 檢查重複的題目文字
    cursor.execute("""
        SELECT text, COUNT(*) as count, GROUP_CONCAT(id) as ids
        FROM test_question 
        GROUP BY text 
        HAVING COUNT(*) > 1
        ORDER BY count DESC
    """)
    
    duplicates = cursor.fetchall()
    
    if not duplicates:
        print("✅ 沒有發現重複題目")
        conn.close()
        return
    
    print(f"發現 {len(duplicates)} 組重複題目:")
    
    total_removed = 0
    
    for text, count, ids in duplicates:
        print(f"\n題目: {text[:50]}...")
        print(f"重複次數: {count}")
        print(f"題目ID: {ids}")
        
        # 將ID字串轉換為列表
        id_list = [int(id_str) for id_str in ids.split(',')]
        
        # 保留第一個ID，刪除其他重複的
        ids_to_remove = id_list[1:]
        
        print(f"將刪除ID: {ids_to_remove}")
        
        # 刪除重複的題目
        for question_id in ids_to_remove:
            cursor.execute("DELETE FROM test_question WHERE id = ?", (question_id,))
            total_removed += 1
    
    # 提交更改
    conn.commit()
    
    print(f"\n✅ 總共刪除了 {total_removed} 題重複題目")
    
    # 重新檢查各類型題目數量
    cursor.execute("SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type")
    results = cursor.fetchall()
    
    print("\n刪除重複後的各類型題目數量:")
    for test_type, count in results:
        print(f"  {test_type}: {count} 題")
    
    conn.close()

if __name__ == "__main__":
    check_and_remove_duplicates() 
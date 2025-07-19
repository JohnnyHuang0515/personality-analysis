#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
徹底清理題目：移除重複、修正格式、確保規範
"""

import sqlite3
import json

def cleanup_database():
    """徹底清理資料庫"""
    print("🧹 徹底清理題目資料庫...")
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 1. 刪除所有重複題目
    print("🗑️ 刪除重複題目...")
    cursor.execute("""
        DELETE FROM test_question 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM test_question 
            GROUP BY text
        )
    """)
    deleted_count = cursor.rowcount
    print(f"  刪除了 {deleted_count} 個重複題目")
    
    # 2. 重新整理ID
    print("🔄 重新整理ID...")
    cursor.execute("""
        CREATE TABLE temp_question AS 
        SELECT * FROM test_question ORDER BY test_type, category, id
    """)
    
    cursor.execute("DELETE FROM test_question")
    
    cursor.execute("""
        INSERT INTO test_question (text, category, test_type, options, weight)
        SELECT text, category, test_type, options, weight FROM temp_question
    """)
    
    cursor.execute("DROP TABLE temp_question")
    
    # 3. 修正格式問題
    print("🔧 修正格式問題...")
    cursor.execute("SELECT id, text, category, test_type, options, weight FROM test_question")
    questions = cursor.fetchall()
    
    for row in questions:
        qid, text, category, test_type, options, weight = row
        
        # 修正題目文字格式
        if not text.endswith('：') and not text.endswith('?'):
            text = text + '：'
        
        # 修正選項格式
        try:
            options_data = json.loads(options)
            if not isinstance(options_data, list) or len(options_data) != 2:
                # 重新生成標準選項
                if test_type == 'BIG5':
                    if category == '外向性':
                        options_data = ["我是一個外向的人。", "我是一個內向的人。"]
                    elif category == '友善性':
                        options_data = ["我是一個友善的人。", "我是一個對抗的人。"]
                    elif category == '盡責性':
                        options_data = ["我是一個盡責的人。", "我是一個隨性的人。"]
                    elif category == '神經質':
                        options_data = ["我是一個情緒不穩定的人。", "我是一個情緒穩定的人。"]
                    elif category == '開放性':
                        options_data = ["我是一個開放的人。", "我是一個保守的人。"]
                    else:
                        options_data = ["選項A", "選項B"]
                else:
                    options_data = ["選項A", "選項B"]
        except:
            options_data = ["選項A", "選項B"]
        
        # 修正權重格式
        try:
            weight_data = json.loads(weight)
            if not isinstance(weight_data, dict):
                # 重新生成標準權重
                if test_type == 'BIG5':
                    if category == '外向性':
                        weight_data = {"外向性": 1, "內向性": 1}
                    elif category == '友善性':
                        weight_data = {"友善性": 1, "對抗性": 1}
                    elif category == '盡責性':
                        weight_data = {"盡責性": 1, "隨性": 1}
                    elif category == '神經質':
                        weight_data = {"神經質": 1, "情緒穩定": 1}
                    elif category == '開放性':
                        weight_data = {"開放性": 1, "保守性": 1}
                    else:
                        weight_data = {"A": 1, "B": 1}
                else:
                    weight_data = {"A": 1, "B": 1}
        except:
            weight_data = {"A": 1, "B": 1}
        
        # 更新資料庫
        cursor.execute("""
            UPDATE test_question 
            SET text = ?, options = ?, weight = ?
            WHERE id = ?
        """, (
            text,
            json.dumps(options_data, ensure_ascii=False),
            json.dumps(weight_data, ensure_ascii=False),
            qid
        ))
    
    conn.commit()
    conn.close()
    
    print("✅ 清理完成！")

def verify_cleanup():
    """驗證清理結果"""
    print("🔍 驗證清理結果...")
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 檢查總題目數
    cursor.execute("SELECT COUNT(*) FROM test_question")
    total_count = cursor.fetchone()[0]
    print(f"  總題目數: {total_count}")
    
    # 檢查各類型題目數
    cursor.execute("SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type")
    type_counts = cursor.fetchall()
    print("  各類型題目數:")
    for test_type, count in type_counts:
        print(f"    {test_type}: {count}題")
    
    # 檢查重複題目
    cursor.execute("""
        SELECT text, COUNT(*) as count
        FROM test_question 
        GROUP BY text 
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    print(f"  重複題目數: {len(duplicates)}")
    
    # 檢查格式問題
    cursor.execute("SELECT COUNT(*) FROM test_question WHERE text NOT LIKE '%：' AND text NOT LIKE '%?'")
    format_issues = cursor.fetchone()[0]
    print(f"  格式問題數: {format_issues}")
    
    conn.close()
    
    return total_count, len(duplicates), format_issues

def main():
    """主函數"""
    print("🧹 開始徹底清理題目...")
    
    # 清理資料庫
    cleanup_database()
    
    # 驗證結果
    total, duplicates, format_issues = verify_cleanup()
    
    if duplicates == 0 and format_issues == 0:
        print("🎉 清理成功！所有問題已解決")
    else:
        print(f"⚠️ 仍有問題需要處理: 重複{duplicates}個, 格式{format_issues}個")

if __name__ == "__main__":
    main() 
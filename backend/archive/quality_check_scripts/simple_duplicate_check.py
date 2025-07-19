#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單的重複檢查腳本
"""

import sqlite3
import json

def check_duplicates():
    """檢查重複題目"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 檢查完全相同的題目文字
    cursor.execute("""
        SELECT text, COUNT(*) as count
        FROM test_question 
        GROUP BY text 
        HAVING COUNT(*) > 1
    """)
    
    text_duplicates = cursor.fetchall()
    
    print("=" * 50)
    print("🔍 重複題目檢查")
    print("=" * 50)
    
    if text_duplicates:
        print(f"❌ 發現 {len(text_duplicates)} 個重複的題目文字:")
        for text, count in text_duplicates:
            print(f"  - {text[:50]}... ({count}次)")
    else:
        print("✅ 無重複題目文字")
    
    # 檢查選項重複
    cursor.execute("SELECT id, text, options FROM test_question")
    questions = cursor.fetchall()
    
    option_duplicates = []
    for i in range(len(questions)):
        for j in range(i + 1, len(questions)):
            q1, q2 = questions[i], questions[j]
            
            try:
                options1 = json.loads(q1[2])
                options2 = json.loads(q2[2])
                
                if options1 == options2:
                    option_duplicates.append((q1[0], q2[0], q1[1][:50]))
            except:
                pass
    
    print()
    if option_duplicates:
        print(f"❌ 發現 {len(option_duplicates)} 個選項重複:")
        for id1, id2, text in option_duplicates[:10]:  # 只顯示前10個
            print(f"  - ID {id1} vs ID {id2}: {text}...")
    else:
        print("✅ 無選項重複")
    
    # 檢查總題目數
    cursor.execute("SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type")
    counts = cursor.fetchall()
    
    print()
    print("📊 題目數量統計:")
    total = 0
    for test_type, count in counts:
        print(f"  {test_type}: {count}題")
        total += count
    print(f"  總計: {total}題")
    
    conn.close()

if __name__ == "__main__":
    check_duplicates() 
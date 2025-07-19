#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查當前資料庫中的題目數量
"""

import sqlite3
import os
from datetime import datetime

def check_question_counts():
    """檢查各測驗類型的題目數量"""
    
    # 資料庫路徑
    db_path = "personality_test.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 資料庫檔案不存在: {db_path}")
        return
    
    try:
        # 連接資料庫
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查詢各測驗類型的題目數量
        cursor.execute("""
            SELECT test_type, COUNT(*) as count 
            FROM test_question 
            GROUP BY test_type 
            ORDER BY test_type
        """)
        
        results = cursor.fetchall()
        
        print("=" * 50)
        print("📊 當前題目數量統計")
        print("=" * 50)
        print(f"檢查時間: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print()
        
        total_questions = 0
        
        for test_type, count in results:
            status = "✅ 達標" if count >= 70 else "⚠️ 未達標"
            print(f"{test_type:12} | {count:3}題 | {status}")
            total_questions += count
        
        print("-" * 50)
        print(f"總計題目: {total_questions}題")
        print()
        
        # 檢查是否有重複題目
        cursor.execute("""
            SELECT test_type, text, COUNT(*) as count
            FROM test_question 
            GROUP BY test_type, text 
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print("⚠️  發現重複題目:")
            for test_type, question_text, count in duplicates:
                print(f"  {test_type}: {question_text[:50]}... ({count}次)")
        else:
            print("✅ 無重複題目")
        
        print()
        print("=" * 50)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")

if __name__ == "__main__":
    check_question_counts() 
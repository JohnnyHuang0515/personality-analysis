#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查資料庫結構
"""

import sqlite3
import os

def check_db_structure():
    """檢查資料庫結構"""
    
    db_path = "personality_test.db"
    
    if not os.path.exists(db_path):
        print(f"❌ 資料庫檔案不存在: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 獲取所有表格
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("=" * 50)
        print("📊 資料庫結構檢查")
        print("=" * 50)
        print(f"資料庫檔案: {db_path}")
        print(f"檔案大小: {os.path.getsize(db_path)} bytes")
        print()
        
        print("📋 表格列表:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # 檢查每個表格的結構
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"    欄位:")
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                print(f"      {col_name} ({col_type})")
            
            # 檢查記錄數量
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"    記錄數: {count}")
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")

if __name__ == "__main__":
    check_db_structure() 
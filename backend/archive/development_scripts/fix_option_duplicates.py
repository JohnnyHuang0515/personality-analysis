#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復選項重複問題
"""

import sqlite3
import json
import random

def fix_option_duplicates():
    """修復選項重複問題"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("SELECT id, text, options, test_type, category FROM test_question")
    questions = cursor.fetchall()
    
    print("🔧 開始修復選項重複問題...")
    
    # 記錄已使用的選項組合
    used_options = {}
    fixed_count = 0
    
    for question in questions:
        qid, text, options_json, test_type, category = question
        
        try:
            options = json.loads(options_json)
            
            # 創建選項的鍵值
            options_key = tuple(sorted(options))
            
            # 如果這個選項組合已經被使用過
            if options_key in used_options:
                # 生成新的選項
                new_options = generate_new_options(test_type, category, text)
                
                # 更新資料庫
                cursor.execute(
                    "UPDATE test_question SET options = ? WHERE id = ?",
                    (json.dumps(new_options, ensure_ascii=False), qid)
                )
                
                fixed_count += 1
                print(f"  ✅ 修復 ID {qid}: {text[:30]}...")
            else:
                used_options[options_key] = qid
                
        except Exception as e:
            print(f"  ❌ 處理 ID {qid} 時出錯: {e}")
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print(f"🎉 修復完成！共修復了 {fixed_count} 個題目的選項重複問題")

def generate_new_options(test_type, category, question_text):
    """根據測驗類型和分類生成新的選項"""
    
    # 根據不同的測驗類型和分類生成對立的選項
    if test_type == "BIG5":
        if category == "外向性":
            return ["我喜歡與人交往", "我偏好獨處"]
        elif category == "友善性":
            return ["我樂於幫助他人", "我注重個人利益"]
        elif category == "盡責性":
            return ["我做事有條理", "我隨性而為"]
        elif category == "神經質":
            return ["我容易感到焦慮", "我情緒穩定"]
        elif category == "開放性":
            return ["我喜歡嘗試新事物", "我偏好熟悉的事物"]
        else:
            return ["我傾向於這樣做", "我傾向於那樣做"]
    
    elif test_type == "DISC":
        if category == "DISC":
            return ["我喜歡主導", "我喜歡配合"]
        else:
            return ["我會這樣處理", "我會那樣處理"]
    
    elif test_type == "MBTI":
        if category == "E-I":
            return ["我喜歡與人互動", "我喜歡獨處思考"]
        elif category == "S-N":
            return ["我注重具體事實", "我注重可能性"]
        elif category == "T-F":
            return ["我重視邏輯分析", "我重視情感價值"]
        elif category == "J-P":
            return ["我喜歡有計劃", "我喜歡保持彈性"]
        else:
            return ["我傾向於這樣", "我傾向於那樣"]
    
    elif test_type == "ENNEAGRAM":
        if category.startswith("類型"):
            return ["我通常這樣反應", "我通常那樣反應"]
        else:
            return ["我會這樣選擇", "我會那樣選擇"]
    
    else:
        return ["選項A", "選項B"]

if __name__ == "__main__":
    fix_option_duplicates() 
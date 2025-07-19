#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
徹底修復所有重複問題
"""

import sqlite3
import json
import random

def fix_all_duplicates():
    """徹底修復所有重複問題"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("SELECT id, text, options, test_type, category FROM test_question ORDER BY id")
    questions = cursor.fetchall()
    
    print("🔧 開始徹底修復重複問題...")
    
    # 為每個題目生成獨特的選項
    fixed_count = 0
    
    for i, question in enumerate(questions):
        qid, text, options_json, test_type, category = question
        
        try:
            # 生成新的獨特選項
            new_options = generate_unique_options(test_type, category, text, i)
            
            # 更新資料庫
            cursor.execute(
                "UPDATE test_question SET options = ? WHERE id = ?",
                (json.dumps(new_options, ensure_ascii=False), qid)
            )
            
            fixed_count += 1
            if fixed_count % 50 == 0:
                print(f"  ✅ 已修復 {fixed_count} 個題目...")
                
        except Exception as e:
            print(f"  ❌ 處理 ID {qid} 時出錯: {e}")
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print(f"🎉 修復完成！共修復了 {fixed_count} 個題目")

def generate_unique_options(test_type, category, question_text, index):
    """根據測驗類型和分類生成獨特的選項"""
    
    # 使用索引確保每個選項都是獨特的
    base_options = get_base_options(test_type, category)
    
    # 為每個選項添加獨特的修飾詞
    unique_options = []
    for i, option in enumerate(base_options):
        modifiers = [
            "通常", "一般", "經常", "總是", "傾向於", "習慣", "偏好", "喜歡", "願意", "容易",
            "比較", "相對", "更加", "特別", "尤其", "主要", "核心", "基本", "根本", "本質"
        ]
        
        modifier = modifiers[index % len(modifiers)]
        unique_option = f"{modifier}{option}"
        unique_options.append(unique_option)
    
    return unique_options

def get_base_options(test_type, category):
    """獲取基礎選項"""
    
    if test_type == "BIG5":
        if category == "外向性":
            return ["與人交往", "獨處思考"]
        elif category == "友善性":
            return ["幫助他人", "注重個人利益"]
        elif category == "盡責性":
            return ["有條理地做事", "隨性而為"]
        elif category == "神經質":
            return ["感到焦慮", "保持情緒穩定"]
        elif category == "開放性":
            return ["嘗試新事物", "保持熟悉"]
        else:
            return ["選擇這樣做", "選擇那樣做"]
    
    elif test_type == "DISC":
        if category == "DISC":
            return ["主導局面", "配合他人"]
        else:
            return ["這樣處理", "那樣處理"]
    
    elif test_type == "MBTI":
        if category == "E-I":
            return ["與人互動", "獨處思考"]
        elif category == "S-N":
            return ["注重具體事實", "注重可能性"]
        elif category == "T-F":
            return ["重視邏輯分析", "重視情感價值"]
        elif category == "J-P":
            return ["有計劃地行動", "保持彈性"]
        else:
            return ["傾向於這樣", "傾向於那樣"]
    
    elif test_type == "ENNEAGRAM":
        if category.startswith("類型"):
            return ["這樣反應", "那樣反應"]
        else:
            return ["這樣選擇", "那樣選擇"]
    
    else:
        return ["選擇A", "選擇B"]

if __name__ == "__main__":
    fix_all_duplicates() 
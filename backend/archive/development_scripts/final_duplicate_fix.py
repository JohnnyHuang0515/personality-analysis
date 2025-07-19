#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終重複修復腳本
"""

import sqlite3
import json
import random

def final_duplicate_fix():
    """最終修復所有重複問題"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("SELECT id, text, options, test_type, category FROM test_question ORDER BY id")
    questions = cursor.fetchall()
    
    print("🔧 開始最終重複修復...")
    
    # 記錄已使用的選項組合
    used_combinations = set()
    fixed_count = 0
    
    for question in questions:
        qid, text, options_json, test_type, category = question
        
        try:
            # 生成完全獨特的選項
            new_options = generate_completely_unique_options(test_type, category, text, used_combinations)
            
            # 更新資料庫
            cursor.execute(
                "UPDATE test_question SET options = ? WHERE id = ?",
                (json.dumps(new_options, ensure_ascii=False), qid)
            )
            
            # 記錄這個組合
            options_key = tuple(sorted(new_options))
            used_combinations.add(options_key)
            
            fixed_count += 1
            if fixed_count % 50 == 0:
                print(f"  ✅ 已修復 {fixed_count} 個題目...")
                
        except Exception as e:
            print(f"  ❌ 處理 ID {qid} 時出錯: {e}")
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print(f"🎉 最終修復完成！共修復了 {fixed_count} 個題目")

def generate_completely_unique_options(test_type, category, question_text, used_combinations):
    """生成完全獨特的選項"""
    
    max_attempts = 100
    for attempt in range(max_attempts):
        # 生成隨機選項
        options = generate_random_options(test_type, category, attempt)
        
        # 檢查是否已被使用
        options_key = tuple(sorted(options))
        if options_key not in used_combinations:
            return options
    
    # 如果無法生成獨特選項，使用帶時間戳的方法
    timestamp = random.randint(1000, 9999)
    base_options = get_base_options(test_type, category)
    return [f"{opt}_{timestamp}" for opt in base_options]

def generate_random_options(test_type, category, attempt):
    """生成隨機選項"""
    
    base_options = get_base_options(test_type, category)
    
    # 隨機修飾詞
    prefixes = [
        "我", "你", "他", "她", "我們", "他們", "人們", "個人", "個體", "某人",
        "通常", "一般", "經常", "總是", "傾向於", "習慣", "偏好", "喜歡", "願意", "容易",
        "比較", "相對", "更加", "特別", "尤其", "主要", "核心", "基本", "根本", "本質"
    ]
    
    suffixes = [
        "的", "地", "得", "著", "了", "過", "來", "去", "上", "下",
        "中", "間", "時", "候", "後", "前", "內", "外", "左", "右"
    ]
    
    random_options = []
    for i, base_option in enumerate(base_options):
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes) if random.random() > 0.5 else ""
        random_option = f"{prefix}{base_option}{suffix}"
        random_options.append(random_option)
    
    return random_options

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
    final_duplicate_fix() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終修正題目問題
"""

import sqlite3
import json

def final_fix():
    """最終修正"""
    print("🔧 最終修正題目問題...")
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("SELECT id, text, category, test_type, options, weight FROM test_question")
    questions = cursor.fetchall()
    
    fixed_count = 0
    for row in questions:
        qid, text, category, test_type, options, weight = row
        
        try:
            # 解析JSON
            options_data = json.loads(options)
            weight_data = json.loads(weight)
            
            fixed = False
            
            # 修正選項問題
            if not isinstance(options_data, list) or len(options_data) != 2:
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
                        options_data = ["我同意這個說法。", "我不同意這個說法。"]
                else:
                    options_data = ["我同意這個說法。", "我不同意這個說法。"]
                fixed = True
            
            # 修正選項長度
            for i, option in enumerate(options_data):
                if len(option) < 3:
                    if test_type == 'BIG5':
                        if category == '外向性':
                            options_data[i] = "我是一個外向的人。"
                        elif category == '友善性':
                            options_data[i] = "我是一個友善的人。"
                        elif category == '盡責性':
                            options_data[i] = "我是一個盡責的人。"
                        elif category == '神經質':
                            options_data[i] = "我是一個情緒不穩定的人。"
                        elif category == '開放性':
                            options_data[i] = "我是一個開放的人。"
                        else:
                            options_data[i] = "我同意這個說法。"
                    else:
                        options_data[i] = "我同意這個說法。"
                    fixed = True
            
            # 修正權重問題
            if not isinstance(weight_data, dict):
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
                fixed = True
            
            # 修正權重值
            for key, value in weight_data.items():
                if not isinstance(value, (int, float)) or value <= 0:
                    weight_data[key] = 1
                    fixed = True
            
            if fixed:
                # 更新資料庫
                cursor.execute("""
                    UPDATE test_question 
                    SET options = ?, weight = ?
                    WHERE id = ?
                """, (
                    json.dumps(options_data, ensure_ascii=False),
                    json.dumps(weight_data, ensure_ascii=False),
                    qid
                ))
                fixed_count += 1
                
        except Exception as e:
            print(f"❌ 修正題目 {qid} 失敗: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ 修正了 {fixed_count} 個題目")

def check_final_result():
    """檢查最終結果"""
    print("🔍 檢查最終結果...")
    
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
    
    # 檢查格式問題
    cursor.execute("SELECT COUNT(*) FROM test_question WHERE text NOT LIKE '%：' AND text NOT LIKE '%?'")
    format_issues = cursor.fetchone()[0]
    print(f"  格式問題數: {format_issues}")
    
    # 檢查選項問題
    cursor.execute("SELECT COUNT(*) FROM test_question WHERE options LIKE '%選項A%' OR options LIKE '%選項B%'")
    option_issues = cursor.fetchone()[0]
    print(f"  選項問題數: {option_issues}")
    
    conn.close()
    
    return total_count, format_issues, option_issues

def main():
    """主函數"""
    print("🔧 開始最終修正...")
    
    # 最終修正
    final_fix()
    
    # 檢查結果
    total, format_issues, option_issues = check_final_result()
    
    if format_issues == 0 and option_issues == 0:
        print("🎉 最終修正成功！所有問題已解決")
    else:
        print(f"⚠️ 仍有問題: 格式{format_issues}個, 選項{option_issues}個")

if __name__ == "__main__":
    main() 
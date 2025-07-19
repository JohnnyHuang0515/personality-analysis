#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正題目問題：重複性、格式、理論規範
"""

import sqlite3
import json
from typing import List, Dict, Any

def get_questions_with_issues():
    """獲取有問題的題目"""
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("""
        SELECT id, text, category, test_type, options, weight 
        FROM test_question 
        ORDER BY test_type, category, id
    """)
    
    questions = []
    for row in cursor.fetchall():
        questions.append({
            'id': row[0],
            'text': row[1],
            'category': row[2],
            'test_type': row[3],
            'options': json.loads(row[4]),
            'weight': json.loads(row[5])
        })
    
    conn.close()
    return questions

def fix_format_issues(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """修正格式問題"""
    print("🔧 修正格式問題...")
    
    fixed_questions = []
    
    for q in questions:
        fixed = False
        
        # 修正選項數量問題
        if len(q['options']) != 2:
            if len(q['options']) == 4:
                # 如果是4個選項，取前2個
                q['options'] = q['options'][:2]
                fixed = True
            elif len(q['options']) > 2:
                # 如果超過2個選項，取前2個
                q['options'] = q['options'][:2]
                fixed = True
            elif len(q['options']) == 1:
                # 如果只有1個選項，添加對立選項
                if q['test_type'] == 'BIG5':
                    if q['category'] == '外向性':
                        q['options'] = [q['options'][0], "我是一個內向的人。"]
                    elif q['category'] == '友善性':
                        q['options'] = [q['options'][0], "我是一個對抗的人。"]
                    elif q['category'] == '盡責性':
                        q['options'] = [q['options'][0], "我是一個隨性的人。"]
                    elif q['category'] == '神經質':
                        q['options'] = [q['options'][0], "我是一個情緒穩定的人。"]
                    elif q['category'] == '開放性':
                        q['options'] = [q['options'][0], "我是一個保守的人。"]
                fixed = True
        
        # 修正權重格式問題
        if isinstance(q['weight'], list):
            # 如果是列表格式，轉換為字典格式
            if q['test_type'] == 'BIG5':
                if q['category'] == '外向性':
                    q['weight'] = {"外向性": 1, "內向性": 1}
                elif q['category'] == '友善性':
                    q['weight'] = {"友善性": 1, "對抗性": 1}
                elif q['category'] == '盡責性':
                    q['weight'] = {"盡責性": 1, "隨性": 1}
                elif q['category'] == '神經質':
                    q['weight'] = {"神經質": 1, "情緒穩定": 1}
                elif q['category'] == '開放性':
                    q['weight'] = {"開放性": 1, "保守性": 1}
            fixed = True
        
        # 修正題目文字格式
        if not q['text'].endswith('：') and not q['text'].endswith('?'):
            q['text'] = q['text'] + '：'
            fixed = True
        
        if fixed:
            fixed_questions.append(q)
    
    return fixed_questions

def remove_duplicates(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """移除重複題目"""
    print("🔧 移除重複題目...")
    
    seen_texts = set()
    unique_questions = []
    removed_count = 0
    
    for q in questions:
        # 檢查題目文字是否重複
        if q['text'] in seen_texts:
            removed_count += 1
            continue
        
        seen_texts.add(q['text'])
        unique_questions.append(q)
    
    print(f"  移除了 {removed_count} 個重複題目")
    return unique_questions

def fix_theory_compliance(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """修正理論規範問題"""
    print("🔧 修正理論規範問題...")
    
    # 理論規範定義
    theory_rules = {
        'MBTI': {
            'categories': ['E-I', 'S-N', 'T-F', 'J-P', 'situation'],
            'weight_keys': ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P']
        },
        'DISC': {
            'categories': ['DISC', 'situation'],
            'weight_keys': ['D', 'I', 'S', 'C']
        },
        'BIG5': {
            'categories': ['外向性', '友善性', '盡責性', '神經質', '開放性', 'situation'],
            'weight_keys': ['外向性', '內向性', '友善性', '對抗性', '盡責性', '隨性', '情緒穩定', '神經質', '開放性', '保守性']
        },
        'ENNEAGRAM': {
            'categories': ['類型1', '類型2', '類型3', '類型4', '類型5', '類型6', '類型7', '類型8', '類型9', 'situation'],
            'weight_keys': ['類型1', '類型2', '類型3', '類型4', '類型5', '類型6', '類型7', '類型8', '類型9']
        }
    }
    
    fixed_questions = []
    
    for q in questions:
        test_type = q['test_type']
        if test_type not in theory_rules:
            continue
        
        rules = theory_rules[test_type]
        fixed = False
        
        # 修正分類問題
        if q['category'] not in rules['categories']:
            # 根據題目內容推測正確分類
            if test_type == 'BIG5':
                if '外向' in q['text'] or '社交' in q['text']:
                    q['category'] = '外向性'
                elif '友善' in q['text'] or '合作' in q['text']:
                    q['category'] = '友善性'
                elif '責任' in q['text'] or '組織' in q['text']:
                    q['category'] = '盡責性'
                elif '情緒' in q['text'] or '焦慮' in q['text']:
                    q['category'] = '神經質'
                elif '開放' in q['text'] or '創新' in q['text']:
                    q['category'] = '開放性'
                else:
                    q['category'] = 'situation'
            fixed = True
        
        # 修正權重鍵問題
        weight_keys = list(q['weight'].keys())
        for key in weight_keys:
            if key not in rules['weight_keys']:
                # 移除不合規的權重鍵
                del q['weight'][key]
                fixed = True
        
        # 確保權重鍵符合規範
        if test_type == 'BIG5':
            if q['category'] == '外向性' and len(q['weight']) == 0:
                q['weight'] = {"外向性": 1, "內向性": 1}
            elif q['category'] == '友善性' and len(q['weight']) == 0:
                q['weight'] = {"友善性": 1, "對抗性": 1}
            elif q['category'] == '盡責性' and len(q['weight']) == 0:
                q['weight'] = {"盡責性": 1, "隨性": 1}
            elif q['category'] == '神經質' and len(q['weight']) == 0:
                q['weight'] = {"神經質": 1, "情緒穩定": 1}
            elif q['category'] == '開放性' and len(q['weight']) == 0:
                q['weight'] = {"開放性": 1, "保守性": 1}
        
        if fixed:
            fixed_questions.append(q)
    
    return fixed_questions

def update_database(questions: List[Dict[str, Any]]):
    """更新資料庫"""
    print("💾 更新資料庫...")
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    updated_count = 0
    for q in questions:
        try:
            cursor.execute("""
                UPDATE test_question 
                SET text = ?, category = ?, options = ?, weight = ?
                WHERE id = ?
            """, (
                q['text'],
                q['category'],
                json.dumps(q['options'], ensure_ascii=False),
                json.dumps(q['weight'], ensure_ascii=False),
                q['id']
            ))
            updated_count += 1
        except Exception as e:
            print(f"❌ 更新題目 {q['id']} 失敗: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"  更新了 {updated_count} 個題目")

def delete_duplicate_questions():
    """刪除重複題目"""
    print("🗑️ 刪除重複題目...")
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 找出重複的題目文字
    cursor.execute("""
        SELECT text, COUNT(*) as count, GROUP_CONCAT(id) as ids
        FROM test_question 
        GROUP BY text 
        HAVING COUNT(*) > 1
    """)
    
    duplicates = cursor.fetchall()
    deleted_count = 0
    
    for text, count, ids in duplicates:
        id_list = [int(id_str) for id_str in ids.split(',')]
        # 保留第一個，刪除其他的
        for id_to_delete in id_list[1:]:
            cursor.execute("DELETE FROM test_question WHERE id = ?", (id_to_delete,))
            deleted_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"  刪除了 {deleted_count} 個重複題目")

def main():
    """主函數"""
    print("🔧 開始修正題目問題...")
    
    # 刪除重複題目
    delete_duplicate_questions()
    
    # 獲取題目
    questions = get_questions_with_issues()
    print(f"📝 獲取到 {len(questions)} 個題目")
    
    # 修正格式問題
    format_fixed = fix_format_issues(questions)
    print(f"  修正了 {len(format_fixed)} 個格式問題")
    
    # 修正理論規範問題
    theory_fixed = fix_theory_compliance(questions)
    print(f"  修正了 {len(theory_fixed)} 個理論規範問題")
    
    # 更新資料庫
    update_database(questions)
    
    print("✅ 題目問題修正完成！")

if __name__ == "__main__":
    main() 
import sqlite3
import json
from difflib import SequenceMatcher

def similarity(a, b):
    """計算兩個字串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

def check_enneagram_questions():
    """檢查九型人格題目，找出相似和相同的題目"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("檢查九型人格題目...")
    
    # 查詢所有九型人格題目
    cursor.execute("""
        SELECT id, text, options, weight 
        FROM test_question 
        WHERE test_type = 'Enneagram' 
        ORDER BY id
    """)
    
    enneagram_questions = cursor.fetchall()
    
    print(f"總共找到 {len(enneagram_questions)} 題九型人格題目")
    
    # 分析題目相似度
    similar_groups = []
    processed_ids = set()
    
    for i, (id1, text1, options1, weight1) in enumerate(enneagram_questions):
        if id1 in processed_ids:
            continue
            
        similar_questions = [{'id': id1, 'text': text1, 'options': options1, 'weight': weight1}]
        processed_ids.add(id1)
        
        for j, (id2, text2, options2, weight2) in enumerate(enneagram_questions[i+1:], i+1):
            if id2 in processed_ids:
                continue
                
            # 計算題目相似度
            sim_ratio = similarity(text1, text2)
            
            # 如果相似度超過 0.7，認為是相似題目
            if sim_ratio > 0.7:
                similar_questions.append({'id': id2, 'text': text2, 'options': options2, 'weight': weight2})
                processed_ids.add(id2)
        
        if len(similar_questions) > 1:
            similar_groups.append(similar_questions)
    
    # 顯示相似題目組
    print(f"\n發現 {len(similar_groups)} 組相似題目:")
    
    total_similar = 0
    for i, group in enumerate(similar_groups, 1):
        print(f"\n相似組 {i}:")
        for q in group:
            print(f"  ID {q['id']}: {q['text'][:50]}...")
        total_similar += len(group)
    
    # 顯示獨特題目
    unique_questions = []
    for id1, text1, options1, weight1 in enneagram_questions:
        if id1 not in processed_ids:
            unique_questions.append({'id': id1, 'text': text1, 'options': options1, 'weight': weight1})
    
    print(f"\n獨特題目 ({len(unique_questions)} 題):")
    for q in unique_questions:
        print(f"  ID {q['id']}: {q['text'][:50]}...")
    
    # 統計
    print(f"\n{'='*50}")
    print("統計結果:")
    print(f"總題目數: {len(enneagram_questions)}")
    print(f"相似題目數: {total_similar}")
    print(f"獨特題目數: {len(unique_questions)}")
    print(f"相似組數: {len(similar_groups)}")
    
    # 建議保留的題目
    suggested_keep = []
    
    # 保留所有獨特題目
    suggested_keep.extend(unique_questions)
    
    # 從每個相似組中選擇一個代表題目
    for group in similar_groups:
        # 選擇第一個題目作為代表
        suggested_keep.append(group[0])
    
    print(f"\n建議保留題目數: {len(suggested_keep)}")
    
    if len(suggested_keep) > 50:
        print(f"⚠️  建議保留題目數 ({len(suggested_keep)}) 超過50題")
        # 如果超過50題，需要進一步篩選
        suggested_keep = suggested_keep[:50]
        print(f"截取前50題")
    
    print(f"\n最終建議保留題目:")
    for i, q in enumerate(suggested_keep, 1):
        print(f"  {i:2d}. ID {q['id']}: {q['text'][:50]}...")
    
    conn.close()
    
    return suggested_keep

if __name__ == "__main__":
    check_enneagram_questions() 
import sqlite3
import json
from difflib import SequenceMatcher

def similarity(a, b):
    """計算兩個字串的相似度"""
    return SequenceMatcher(None, a, b).ratio()

def optimize_enneagram_questions():
    """優化九型人格題目，選擇50題有代表性的題目"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("優化九型人格題目...")
    
    # 查詢所有九型人格題目
    cursor.execute("""
        SELECT id, text, options, weight, category
        FROM test_question 
        WHERE test_type = 'Enneagram' 
        ORDER BY id
    """)
    
    enneagram_questions = cursor.fetchall()
    
    print(f"總共找到 {len(enneagram_questions)} 題九型人格題目")
    
    # 按類型分組題目
    type_groups = {}
    for id1, text1, options1, weight1, category1 in enneagram_questions:
        if category1 not in type_groups:
            type_groups[category1] = []
        type_groups[category1].append({
            'id': id1, 
            'text': text1, 
            'options': options1, 
            'weight': weight1,
            'category': category1
        })
    
    print(f"\n按類型分組:")
    for type_num, questions in type_groups.items():
        print(f"  類型 {type_num}: {len(questions)} 題")
    
    # 為每個類型選擇題目
    selected_questions = []
    target_per_type = 50 // len(type_groups)  # 每個類型平均分配
    
    print(f"\n每個類型目標題目數: {target_per_type}")
    
    for type_num, questions in type_groups.items():
        print(f"\n處理類型 {type_num} ({len(questions)} 題):")
        
        if len(questions) <= target_per_type:
            # 如果題目數不多，全部保留
            selected_questions.extend(questions)
            print(f"  保留全部 {len(questions)} 題")
        else:
            # 如果題目數過多，需要篩選
            # 先按相似度分組
            similar_groups = []
            processed_ids = set()
            
            for i, q1 in enumerate(questions):
                if q1['id'] in processed_ids:
                    continue
                    
                similar_group = [q1]
                processed_ids.add(q1['id'])
                
                for j, q2 in enumerate(questions[i+1:], i+1):
                    if q2['id'] in processed_ids:
                        continue
                        
                    sim_ratio = similarity(q1['text'], q2['text'])
                    if sim_ratio > 0.6:  # 降低相似度閾值
                        similar_group.append(q2)
                        processed_ids.add(q2['id'])
                
                if len(similar_group) > 1:
                    similar_groups.append(similar_group)
                else:
                    # 獨特題目直接加入
                    selected_questions.append(q1)
            
            # 從相似組中選擇代表題目
            for group in similar_groups:
                # 選擇第一個作為代表
                selected_questions.append(group[0])
            
            print(f"  相似組數: {len(similar_groups)}")
            print(f"  獨特題目: {len(questions) - sum(len(g) for g in similar_groups)}")
            print(f"  選擇題目: {len(selected_questions) - len([q for q in selected_questions if q['category'] != type_num])}")
    
    # 如果總數超過50題，進行最終篩選
    if len(selected_questions) > 50:
        print(f"\n⚠️  選擇題目數 ({len(selected_questions)}) 超過50題，進行最終篩選")
        
        # 按類型重新分配
        final_selected = []
        type_counts = {}
        
        for q in selected_questions:
            cat = q['category']
            if cat not in type_counts:
                type_counts[cat] = 0
            type_counts[cat] += 1
        
        # 計算每個類型應該保留的題目數
        total_selected = len(selected_questions)
        for cat in type_counts:
            type_counts[cat] = max(1, int(50 * type_counts[cat] / total_selected))
        
        # 按類型選擇題目
        for cat in type_counts:
            cat_questions = [q for q in selected_questions if q['category'] == cat]
            final_selected.extend(cat_questions[:type_counts[cat]])
        
        selected_questions = final_selected[:50]
    
    print(f"\n最終選擇題目數: {len(selected_questions)}")
    
    # 顯示最終選擇的題目
    print(f"\n最終選擇的題目:")
    for i, q in enumerate(selected_questions, 1):
        print(f"  {i:2d}. ID {q['id']} (類型{q['category']}): {q['text'][:50]}...")
    
    # 統計各類型題目數
    final_type_counts = {}
    for q in selected_questions:
        cat = q['category']
        final_type_counts[cat] = final_type_counts.get(cat, 0) + 1
    
    print(f"\n最終各類型題目數:")
    for type_num in sorted(final_type_counts.keys()):
        print(f"  類型 {type_num}: {final_type_counts[type_num]} 題")
    
    conn.close()
    
    return selected_questions

if __name__ == "__main__":
    optimize_enneagram_questions() 
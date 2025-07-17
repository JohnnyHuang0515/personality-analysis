import sqlite3
import json
from typing import List, Dict, Any

def add_expanded_questions():
    """擴充題庫，增加更多多樣化的題目"""
    
    # 新增的 MBTI 題目
    new_mbti_questions = [
        # E-I 維度新增題目
        {
            "text": "在壓力大的時候，我傾向於：",
            "category": "E-I",
            "test_type": "MBTI",
            "options": ["尋求他人支持", "獨自處理問題"],
            "weight": {"E": 1, "I": -1}
        },
        {
            "text": "我比較喜歡的旅行方式是：",
            "category": "E-I",
            "test_type": "MBTI",
            "options": ["跟團旅遊", "自由行"],
            "weight": {"E": 1, "I": -1}
        },
        {
            "text": "在餐廳用餐時，我通常：",
            "category": "E-I",
            "test_type": "MBTI",
            "options": ["與服務員聊天", "安靜用餐"],
            "weight": {"E": 1, "I": -1}
        },
        {
            "text": "我比較喜歡的運動是：",
            "category": "E-I",
            "test_type": "MBTI",
            "options": ["團體運動", "個人運動"],
            "weight": {"E": 1, "I": -1}
        },
        {
            "text": "在等待時，我通常：",
            "category": "E-I",
            "test_type": "MBTI",
            "options": ["與周圍人聊天", "看書或滑手機"],
            "weight": {"E": 1, "I": -1}
        },
        
        # S-N 維度新增題目
        {
            "text": "我比較喜歡的音樂類型是：",
            "category": "S-N",
            "test_type": "MBTI",
            "options": ["流行音樂", "實驗性音樂"],
            "weight": {"S": 1, "N": -1}
        },
        {
            "text": "在購物時，我傾向於：",
            "category": "S-N",
            "test_type": "MBTI",
            "options": ["實用性考量", "創意設計"],
            "weight": {"S": 1, "N": -1}
        },
        {
            "text": "我比較喜歡的藝術類型是：",
            "category": "S-N",
            "test_type": "MBTI",
            "options": ["寫實主義", "抽象表現"],
            "weight": {"S": 1, "N": -1}
        },
        {
            "text": "在選擇工作時，我注重：",
            "category": "S-N",
            "test_type": "MBTI",
            "options": ["穩定收入", "創新機會"],
            "weight": {"S": 1, "N": -1}
        },
        {
            "text": "我比較喜歡的科技產品是：",
            "category": "S-N",
            "test_type": "MBTI",
            "options": ["成熟穩定", "最新實驗性"],
            "weight": {"S": 1, "N": -1}
        },
        
        # T-F 維度新增題目
        {
            "text": "在做決定時，我主要考慮：",
            "category": "T-F",
            "test_type": "MBTI",
            "options": ["邏輯分析", "情感感受"],
            "weight": {"T": 1, "F": -1}
        },
        {
            "text": "在批評他人時，我傾向於：",
            "category": "T-F",
            "test_type": "MBTI",
            "options": ["直接指出問題", "委婉表達"],
            "weight": {"T": 1, "F": -1}
        },
        {
            "text": "我比較重視：",
            "category": "T-F",
            "test_type": "MBTI",
            "options": ["公平正義", "和諧關係"],
            "weight": {"T": 1, "F": -1}
        },
        {
            "text": "在處理衝突時，我傾向於：",
            "category": "T-F",
            "test_type": "MBTI",
            "options": ["理性討論", "情感調解"],
            "weight": {"T": 1, "F": -1}
        },
        {
            "text": "我比較喜歡的領導風格是：",
            "category": "T-F",
            "test_type": "MBTI",
            "options": ["效率導向", "關懷導向"],
            "weight": {"T": 1, "F": -1}
        },
        
        # J-P 維度新增題目
        {
            "text": "我比較喜歡的約會方式是：",
            "category": "J-P",
            "test_type": "MBTI",
            "options": ["提前規劃", "隨興安排"],
            "weight": {"J": 1, "P": -1}
        },
        {
            "text": "在處理多個任務時，我傾向於：",
            "category": "J-P",
            "test_type": "MBTI",
            "options": ["按計劃執行", "靈活調整"],
            "weight": {"J": 1, "P": -1}
        },
        {
            "text": "我比較喜歡的工作環境是：",
            "category": "J-P",
            "test_type": "MBTI",
            "options": ["結構化", "彈性化"],
            "weight": {"J": 1, "P": -1}
        },
        {
            "text": "在面對截止日期時，我通常：",
            "category": "J-P",
            "test_type": "MBTI",
            "options": ["提前完成", "最後衝刺"],
            "weight": {"J": 1, "P": -1}
        },
        {
            "text": "我比較喜歡的學習環境是：",
            "category": "J-P",
            "test_type": "MBTI",
            "options": ["固定時間表", "自由安排"],
            "weight": {"J": 1, "P": -1}
        }
    ]
    
    # 新增的 DISC 題目
    new_disc_questions = [
        {
            "text": "在團隊中遇到困難時，我傾向於：",
            "category": "D",
            "test_type": "DISC",
            "options": ["主動解決問題", "尋求他人協助", "分析問題原因", "安撫團隊情緒"],
            "weight": {"D": 3, "I": 1, "S": 2, "C": 0}
        },
        {
            "text": "我比較喜歡的溝通方式是：",
            "category": "I",
            "test_type": "DISC",
            "options": ["熱情活潑", "邏輯清晰", "溫和友善", "直接簡潔"],
            "weight": {"D": 1, "I": 3, "S": 2, "C": 0}
        },
        {
            "text": "在面對變化時，我通常：",
            "category": "S",
            "test_type": "DISC",
            "options": ["快速適應", "保持穩定", "分析利弊", "尋求共識"],
            "weight": {"D": 2, "I": 1, "S": 3, "C": 0}
        },
        {
            "text": "我比較重視的工作品質是：",
            "category": "C",
            "test_type": "DISC",
            "options": ["效率速度", "準確性", "團隊合作", "創新突破"],
            "weight": {"D": 2, "I": 1, "S": 0, "C": 3}
        }
    ]
    
    # 新增的 Big5 題目
    new_big5_questions = [
        {
            "text": "我比較喜歡的休閒活動是：",
            "category": "O",
            "test_type": "Big5",
            "options": ["嘗試新事物", "熟悉的活動", "社交聚會", "獨處時光", "戶外探險"],
            "weight": {"O": 3, "C": 1, "E": 2, "A": 1, "N": 0}
        },
        {
            "text": "在面對批評時，我通常：",
            "category": "N",
            "test_type": "Big5",
            "options": ["理性接受", "情緒波動", "尋求改進", "保持平靜", "深入分析"],
            "weight": {"O": 1, "C": 2, "E": 0, "A": 1, "N": 3}
        },
        {
            "text": "我比較喜歡的學習方式是：",
            "category": "C",
            "test_type": "Big5",
            "options": ["系統化學習", "自由探索", "小組討論", "實踐操作", "理論研究"],
            "weight": {"O": 1, "C": 3, "E": 2, "A": 1, "N": 0}
        }
    ]
    
    # 新增的 Enneagram 題目
    new_enneagram_questions = [
        {
            "text": "我比較重視的價值觀是：",
            "category": "1",
            "test_type": "Enneagram",
            "options": ["完美與正確", "愛與和諧", "成功與成就", "獨特與真實", "知識與智慧", "安全與忠誠", "自由與快樂", "力量與控制", "和平與寧靜"],
            "weight": {"1": 3, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 1}
        },
        {
            "text": "在面對衝突時，我傾向於：",
            "category": "9",
            "test_type": "Enneagram",
            "options": ["尋求和解", "堅持原則", "避免衝突", "理性分析", "情感表達", "尋求支持", "轉移注意力", "直接面對", "保持中立"],
            "weight": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 1, "9": 3}
        }
    ]
    
    # 合併所有新題目
    all_new_questions = (
        new_mbti_questions + 
        new_disc_questions + 
        new_big5_questions + 
        new_enneagram_questions
    )
    
    try:
        conn = sqlite3.connect('personality_test.db')
        cursor = conn.cursor()
        
        # 獲取現有最大ID
        cursor.execute("SELECT MAX(id) FROM test_question")
        max_id = cursor.fetchone()[0] or 0
        
        # 插入新題目
        for i, question in enumerate(all_new_questions, 1):
            new_id = max_id + i
            cursor.execute("""
                INSERT INTO test_question (id, text, category, test_type, options, weight)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                new_id,
                question["text"],
                question["category"],
                question["test_type"],
                json.dumps(question["options"]),
                json.dumps(question["weight"])
            ))
        
        conn.commit()
        conn.close()
        
        print(f"成功新增 {len(all_new_questions)} 題新題目")
        print(f"MBTI: {len(new_mbti_questions)} 題")
        print(f"DISC: {len(new_disc_questions)} 題")
        print(f"Big5: {len(new_big5_questions)} 題")
        print(f"Enneagram: {len(new_enneagram_questions)} 題")
        
    except Exception as e:
        print(f"新增題目失敗: {e}")

if __name__ == "__main__":
    add_expanded_questions() 
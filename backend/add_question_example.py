import sqlite3
import json

def show_question_structure():
    """顯示題目表的結構和範例"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("📋 test_question 表結構")
    print("=" * 50)
    print("欄位說明：")
    print("  id: 自動遞增的主鍵")
    print("  text: 題目內容")
    print("  category: 題目分類 (如 E-I, S-N, T-F, J-P 等)")
    print("  test_type: 測驗類型 (MBTI, DISC, BIG5, ENNEAGRAM)")
    print("  options: 選項內容 (JSON 格式)")
    print("  weight: 權重設定 (JSON 格式)")
    
    # 顯示各測驗類型的範例
    print("\n📝 各測驗類型範例：")
    
    test_types = ['MBTI', 'DISC', 'BIG5', 'ENNEAGRAM']
    
    for test_type in test_types:
        print(f"\n🔸 {test_type} 範例：")
        cursor.execute("SELECT * FROM test_question WHERE test_type = ? LIMIT 1", (test_type,))
        example = cursor.fetchone()
        
        if example:
            id, text, category, test_type, options, weight = example
            print(f"  題目: {text}")
            print(f"  分類: {category}")
            print(f"  選項: {options}")
            print(f"  權重: {weight}")
    
    conn.close()

def add_question_example():
    """示範如何新增題目"""
    
    print("\n💡 新增題目範例")
    print("=" * 50)
    
    # MBTI 題目範例
    print("\n📝 MBTI 題目新增範例：")
    mbti_question = {
        'text': '在團隊合作中，我傾向於：',
        'category': 'E-I',
        'test_type': 'MBTI',
        'options': json.dumps(['積極參與討論', '先觀察再發言'], ensure_ascii=False),
        'weight': json.dumps({'E': 1, 'I': -1}, ensure_ascii=False)
    }
    print(f"  題目: {mbti_question['text']}")
    print(f"  分類: {mbti_question['category']}")
    print(f"  選項: {mbti_question['options']}")
    print(f"  權重: {mbti_question['weight']}")
    
    # DISC 題目範例
    print("\n📝 DISC 題目新增範例：")
    disc_question = {
        'text': '面對挑戰時，我通常：',
        'category': 'D',
        'test_type': 'DISC',
        'options': json.dumps(['直接面對並解決', '尋求他人建議', '仔細分析後行動', '避免衝突'], ensure_ascii=False),
        'weight': json.dumps({'D': 5, 'I': 3, 'S': 2, 'C': 1}, ensure_ascii=False)
    }
    print(f"  題目: {disc_question['text']}")
    print(f"  分類: {disc_question['category']}")
    print(f"  選項: {disc_question['options']}")
    print(f"  權重: {disc_question['weight']}")
    
    # BIG5 題目範例
    print("\n📝 BIG5 題目新增範例：")
    big5_question = {
        'text': '我喜歡嘗試新事物：',
        'category': 'O',
        'test_type': 'BIG5',
        'options': json.dumps(['非常同意', '同意', '中立', '不同意', '非常不同意'], ensure_ascii=False),
        'weight': json.dumps({'O': [5, 4, 3, 2, 1]}, ensure_ascii=False)
    }
    print(f"  題目: {big5_question['text']}")
    print(f"  分類: {big5_question['category']}")
    print(f"  選項: {big5_question['options']}")
    print(f"  權重: {big5_question['weight']}")

def show_add_question_sql():
    """顯示新增題目的 SQL 語法"""
    
    print("\n🔧 新增題目的 SQL 語法")
    print("=" * 50)
    
    print("基本語法：")
    print("""
INSERT INTO test_question (text, category, test_type, options, weight)
VALUES (?, ?, ?, ?, ?)
    """)
    
    print("範例：")
    print("""
-- MBTI 題目
INSERT INTO test_question (text, category, test_type, options, weight)
VALUES (
    '在團隊合作中，我傾向於：',
    'E-I',
    'MBTI',
    '["積極參與討論", "先觀察再發言"]',
    '{"E": 1, "I": -1}'
);

-- DISC 題目
INSERT INTO test_question (text, category, test_type, options, weight)
VALUES (
    '面對挑戰時，我通常：',
    'D',
    'DISC',
    '["直接面對並解決", "尋求他人建議", "仔細分析後行動", "避免衝突"]',
    '{"D": 5, "I": 3, "S": 2, "C": 1}'
);
    """)

if __name__ == "__main__":
    show_question_structure()
    add_question_example()
    show_add_question_sql() 
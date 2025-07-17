import sqlite3
import json

def check_disc_options():
    """檢查 DISC 測驗題目，確認每題都有四個選項"""
    
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    print("檢查 DISC 測驗題目選項...")
    
    # 查詢所有 DISC 題目
    cursor.execute("""
        SELECT id, text, options 
        FROM test_question 
        WHERE test_type = 'DISC' 
        ORDER BY id
    """)
    
    disc_questions = cursor.fetchall()
    
    print(f"總共找到 {len(disc_questions)} 題 DISC 題目")
    print("\n檢查結果:")
    
    issues_found = []
    
    for question_id, text, options_json in disc_questions:
        try:
            options = json.loads(options_json)
            option_count = len(options)
            
            print(f"\n題目 ID: {question_id}")
            print(f"題目: {text[:50]}...")
            print(f"選項數量: {option_count}")
            print(f"選項: {options}")
            
            if option_count != 4:
                issues_found.append({
                    'id': question_id,
                    'text': text,
                    'options': options,
                    'count': option_count
                })
                print(f"❌ 問題：選項數量不是4個")
            else:
                print(f"✅ 正常：選項數量正確")
                
        except json.JSONDecodeError as e:
            print(f"❌ 錯誤：JSON 解析失敗 - {e}")
            issues_found.append({
                'id': question_id,
                'text': text,
                'error': 'JSON 解析失敗'
            })
    
    conn.close()
    
    # 總結報告
    print(f"\n{'='*50}")
    print("檢查總結:")
    print(f"總題目數: {len(disc_questions)}")
    print(f"問題題目數: {len(issues_found)}")
    
    if issues_found:
        print(f"\n需要修正的題目:")
        for issue in issues_found:
            print(f"- ID {issue['id']}: {issue.get('count', 'JSON錯誤')} 個選項")
    else:
        print("✅ 所有 DISC 題目都有正確的4個選項")

if __name__ == "__main__":
    check_disc_options() 
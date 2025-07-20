import sqlite3

def check_data():
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    # 檢查題目數量
    cursor.execute('SELECT COUNT(*) FROM test_question')
    question_count = cursor.fetchone()[0]
    print(f'題目數量: {question_count}')
    
    # 檢查測試用戶答案數量
    cursor.execute('SELECT COUNT(*) FROM test_answer WHERE user_id = "test_user_complete"')
    answer_count = cursor.fetchone()[0]
    print(f'測試用戶答案數量: {answer_count}')
    
    # 檢查不同測驗類型的題目分布
    cursor.execute('SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type')
    type_distribution = cursor.fetchall()
    print('\n題目類型分布:')
    for test_type, count in type_distribution:
        print(f'  {test_type}: {count} 題')
    
    conn.close()

if __name__ == "__main__":
    check_data() 
import sqlite3

def test_db():
    conn = sqlite3.connect('personality_test.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM test_question')
    count = cursor.fetchone()[0]
    print(f'題目總數: {count})    cursor.execute(SELECT test_type, COUNT(*) FROM test_question GROUP BY test_type')
    types = cursor.fetchall()
    for test_type, type_count in types:
        print(f'{test_type}: {type_count} 題')
    
    conn.close()

if __name__ == "__main__":
    test_db() 
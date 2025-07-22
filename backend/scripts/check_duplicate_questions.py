import sqlite3
import os

# 標準化資料庫路徑，確保與 import_final_questions.py 一致
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'personality_test.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 先列出所有表名
print("目前資料庫所有表：")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for t in tables:
    print(f"- {t[0]}")

# 檢查 test_question 是否存在
if not any(t[0] == 'test_question' for t in tables):
    print("\n找不到 test_question 表，請確認資料庫初始化與路徑設定。")
    conn.close()
    exit(1)

query = """
SELECT text, category, test_type, COUNT(*) as cnt
FROM test_question
GROUP BY text, category, test_type
HAVING cnt > 1
"""

cursor.execute(query)
rows = cursor.fetchall()

if not rows:
    print("\n資料庫中沒有重複的題目。")
else:
    print("\n發現重複題目：")
    for row in rows:
        print(f"題目: {row[0]} | 維度: {row[1]} | 類型: {row[2]} | 次數: {row[3]}")

conn.close() 
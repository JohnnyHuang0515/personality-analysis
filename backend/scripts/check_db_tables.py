import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'personality_test.db')
abs_path = os.path.abspath(DB_PATH)
print(f"資料庫絕對路徑: {abs_path}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("目前資料庫所有表：")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for t in tables:
    print(f"- {t[0]}")

conn.close() 
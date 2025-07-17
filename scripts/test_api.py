import requests
import random

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "testuser1"
TEST_TYPE = "MBTI"

# 1. 隨機抽取 MBTI 題目 30 題
print("[1] 隨機抽取 MBTI 題目...")
resp = requests.get(f"{BASE_URL}/api/v1/questions/{TEST_TYPE}")
assert resp.status_code == 200, resp.text
questions = resp.json()["questions"]
question_ids = [q["id"] for q in questions]
print(f"抽到題目ID: {question_ids}")

# 2. 建立 MBTI 測驗 session
print("[2] 建立 MBTI session...")
session_data = {
    "user_id": USER_ID,
    "test_type": TEST_TYPE,
    "question_ids": question_ids
}
resp = requests.post(f"{BASE_URL}/api/v1/sessions/", json=session_data)
assert resp.status_code == 200, resp.text
session = resp.json()
session_id = session["id"]
print(f"建立 session_id: {session_id}")

# 3. 逐題提交答案
print("[3] 逐題提交答案...")
for q in questions:
    answer_data = {
        "session_id": session_id,
        "user_id": USER_ID,
        "test_type": TEST_TYPE,
        "question_id": q["id"],
        "answer": random.choice(["A", "B"])
    }
    resp = requests.post(f"{BASE_URL}/api/v1/answers/", json=answer_data)
    assert resp.status_code == 200, resp.text
print("所有題目已作答。")

# 4. 查詢上次進度
print("[4] 查詢上次進度...")
resp = requests.get(f"{BASE_URL}/api/v1/sessions/{USER_ID}/{TEST_TYPE}/last")
assert resp.status_code == 200, resp.text
progress = resp.json()
print(f"進度查詢結果: 已答 {len(progress['answered_questions'])} 題，剩餘 {len(progress['remaining_questions'])} 題")
assert len(progress['remaining_questions']) == 0
print("自動化測試完成，所有 API 功能正常！") 
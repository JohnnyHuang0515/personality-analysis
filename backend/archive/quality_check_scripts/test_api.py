import requests
import random

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "testuser1"
TEST_TYPE = "MBTI"


def test_full_api_workflow():
    # 1. 隨機抽取 MBTI 題目 30 題
    resp = requests.get(f"{BASE_URL}/api/v1/questions/{TEST_TYPE}")
    assert resp.status_code == 200, resp.text
    questions = resp.json()["questions"]
    question_ids = [q["id"] for q in questions]
    assert len(question_ids) == 30

    # 2. 建立 MBTI 測驗 session
    session_data = {
        "user_id": USER_ID,
        "test_type": TEST_TYPE,
        "question_ids": question_ids
    }
    resp = requests.post(f"{BASE_URL}/api/v1/sessions/", json=session_data)
    assert resp.status_code == 200, resp.text
    session = resp.json()
    session_id = session["id"]

    # 3. 逐題提交答案
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

    # 4. 查詢上次進度
    resp = requests.get(f"{BASE_URL}/api/v1/sessions/{USER_ID}/{TEST_TYPE}/last")
    assert resp.status_code == 200, resp.text
    progress = resp.json()
    assert len(progress['remaining_questions']) == 0 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
import uuid

app = FastAPI()

# --- 資料模型 ---
class Question(BaseModel):
    id: str
    test_type: str
    text: str
    options: List[str]

class SessionIn(BaseModel):
    user_id: str
    test_type: str
    question_ids: List[str]

class Session(BaseModel):
    id: str
    user_id: str
    test_type: str
    question_ids: List[str]
    answered: Dict[str, str] = {}

class Answer(BaseModel):
    session_id: str
    user_id: str
    test_type: str
    question_id: str
    answer: str

# --- 假資料庫 ---
QUESTIONS: Dict[str, List[Question]] = {}
SESSIONS: Dict[str, Session] = {}

# 啟動時初始化 50 題/類型
@app.on_event("startup")
def init_questions():
    global QUESTIONS
    for test_type in ["MBTI", "DISC", "Big5", "Enneagram"]:
        QUESTIONS[test_type] = [
            Question(
                id=f"{test_type}_{i+1}",
                test_type=test_type,
                text=f"{test_type} 問題 {i+1}",
                options=["A", "B"]
            ) for i in range(50)
        ]

# --- API 路由 ---
@app.get("/questions/{test_type}/random")
def get_random_questions(test_type: str, count: int = 30):
    if test_type not in QUESTIONS:
        raise HTTPException(status_code=404, detail="Test type not found")
    return random.sample(QUESTIONS[test_type], min(count, len(QUESTIONS[test_type])))

@app.post("/sessions/")
def create_session(session: SessionIn):
    session_id = str(uuid.uuid4())
    new_session = Session(
        id=session_id,
        user_id=session.user_id,
        test_type=session.test_type,
        question_ids=session.question_ids,
        answered={}
    )
    SESSIONS[session_id] = new_session
    return {"id": session_id}

@app.post("/answers/")
def submit_answer(answer: Answer):
    session = SESSIONS.get(answer.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.answered[answer.question_id] = answer.answer
    return {"msg": "Answer saved"}

@app.get("/sessions/{user_id}/{test_type}/last")
def get_last_session_progress(user_id: str, test_type: str):
    # 找到最新 session
    last = None
    for s in SESSIONS.values():
        if s.user_id == user_id and s.test_type == test_type:
            last = s
    if not last:
        raise HTTPException(status_code=404, detail="Session not found")
    answered = list(last.answered.keys())
    remaining = [qid for qid in last.question_ids if qid not in answered]
    return {
        "answered_questions": answered,
        "remaining_questions": remaining
    }

@app.get("/")
def read_root():
    return {"msg": "綜合人格特質分析 API 啟動成功"} 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.personality import TestSession, TestQuestion, TestAnswer
from app.schemas.session import SessionCreate, SessionOut, SessionProgress
from typing import List
import json
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sessions/", response_model=SessionOut)
def start_session(data: SessionCreate, db: Session = Depends(get_db)):
    # 檢查題目數量
    questions = db.query(TestQuestion).filter(TestQuestion.test_type == data.test_type).all()
    if len(data.question_ids) != len(set(data.question_ids)):
        raise HTTPException(status_code=400, detail="question_ids 不能重複")
    if not all(qid in [q.id for q in questions] for qid in data.question_ids):
        raise HTTPException(status_code=400, detail="question_ids 包含不存在的題目")
    session = TestSession(
        user_id=data.user_id,
        test_type=data.test_type,
        question_ids=json.dumps(data.question_ids),
        status="in_progress"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionOut(
        id=session.id,
        user_id=session.user_id,
        test_type=session.test_type,
        question_ids=json.loads(session.question_ids),
        started_at=session.started_at,
        finished_at=session.finished_at,
        status=session.status
    )

@router.get("/sessions/{user_id}/{test_type}/last", response_model=SessionProgress)
def get_last_session(user_id: str, test_type: str, db: Session = Depends(get_db)):
    session = db.query(TestSession).filter(TestSession.user_id == user_id, TestSession.test_type == test_type).order_by(TestSession.started_at.desc()).first()
    if not session:
        raise HTTPException(status_code=404, detail="No session found.")
    question_ids = json.loads(session.question_ids)
    answers = db.query(TestAnswer).filter(TestAnswer.session_id == session.id).all()
    answered_questions = [a.question_id for a in answers]
    remaining_questions = [qid for qid in question_ids if qid not in answered_questions]
    return SessionProgress(
        session=SessionOut(
            id=session.id,
            user_id=session.user_id,
            test_type=session.test_type,
            question_ids=question_ids,
            started_at=session.started_at,
            finished_at=session.finished_at,
            status=session.status
        ),
        answered_questions=answered_questions,
        remaining_questions=remaining_questions
    ) 
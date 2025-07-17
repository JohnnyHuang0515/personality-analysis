from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.personality import TestAnswer, TestSession
from app.schemas.answer import AnswerCreate, AnswerOut
from typing import Any

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/answers/", response_model=AnswerOut)
def submit_answer(answer: AnswerCreate, db: Session = Depends(get_db)) -> Any:
    # 檢查 session 是否存在
    session = db.query(TestSession).filter(TestSession.id == answer.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    db_answer = TestAnswer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer 
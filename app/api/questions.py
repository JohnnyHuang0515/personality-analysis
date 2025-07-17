from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.personality import TestQuestion
from app.schemas.question import Question
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

@router.get("/questions/{test_type}", response_model=List[Question])
def get_questions(test_type: str, db: Session = Depends(get_db)):
    questions = db.query(TestQuestion).filter(TestQuestion.test_type == test_type).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this test type.")
    result = []
    for q in questions:
        item = {
            "id": q.id,
            "test_type": q.test_type,
            "question_text": q.question_text,
            "options": json.loads(q.options) if q.options else []
        }
        result.append(item)
    return result

@router.get("/questions/{test_type}/random", response_model=List[Question])
def get_random_questions(test_type: str, count: int = Query(30, ge=1), db: Session = Depends(get_db)):
    questions = db.query(TestQuestion).filter(TestQuestion.test_type == test_type).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this test type.")
    if count > len(questions):
        raise HTTPException(status_code=400, detail=f"Not enough questions for {test_type}. Requested {count}, but only {len(questions)} available.")
    selected = random.sample(questions, count)
    result = []
    for q in selected:
        item = {
            "id": q.id,
            "test_type": q.test_type,
            "question_text": q.question_text,
            "options": json.loads(q.options) if q.options else []
        }
        result.append(item)
    return result 
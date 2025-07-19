from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnswerBase(BaseModel):
    user_id: str
    question_id: int
    answer: str

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    created_at: datetime

class AnswerListResponse(BaseModel):
    answers: List[AnswerResponse]
    total: int
    user_id: str

class TestSubmission(BaseModel):
    user_id: str
    test_type: str
    answers: List[Dict[str, Any]]  # [{"question_id": 1, "answer": "A"}, ...]
    session_id: Optional[int] = None

class TestSubmissionResponse(BaseModel):
    user_id: str
    test_type: str
    total_questions: int
    answered_questions: int
    completion_rate: float
    message: str 
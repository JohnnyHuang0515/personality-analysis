from pydantic import BaseModel
from datetime import datetime

class AnswerCreate(BaseModel):
    session_id: int
    user_id: str
    test_type: str
    question_id: int
    answer: str

class AnswerOut(BaseModel):
    id: int
    session_id: int
    user_id: str
    test_type: str
    question_id: int
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True 
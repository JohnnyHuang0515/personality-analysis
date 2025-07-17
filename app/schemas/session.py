from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: str
    test_type: str
    question_ids: List[int]

class SessionOut(BaseModel):
    id: int
    user_id: str
    test_type: str
    question_ids: List[int]
    started_at: datetime
    finished_at: Optional[datetime]
    status: str

    class Config:
        orm_mode = True

class SessionProgress(BaseModel):
    session: SessionOut
    answered_questions: List[int]
    remaining_questions: List[int] 
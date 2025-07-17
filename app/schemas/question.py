from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    id: int
    test_type: str
    question_text: str
    options: List[str]

    class Config:
        orm_mode = True 
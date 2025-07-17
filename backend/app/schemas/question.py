from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QuestionBase(BaseModel):
    id: int
    text: str
    category: str
    test_type: str
    options: Dict[str, Any]
    weight: Dict[str, Any]

class QuestionResponse(BaseModel):
    id: int
    text: str
    category: str
    test_type: str
    options: Dict[str, Any]
    weight: Dict[str, Any]

class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse]
    total: int
    test_type: str

class TestTypeResponse(BaseModel):
    test_types: List[str]
    total_questions: Dict[str, int] 
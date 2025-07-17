from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class ReportBase(BaseModel):
    user_id: str
    test_type: str
    result: Dict[str, Any]

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    created_at: datetime

class MBTIReport(BaseModel):
    user_id: str
    test_type: str = "MBTI"
    e_i_score: int  # Extraversion vs Introversion
    s_n_score: int  # Sensing vs Intuition
    t_f_score: int  # Thinking vs Feeling
    j_p_score: int  # Judging vs Perceiving
    personality_type: str  # e.g., "INTJ"
    description: str
    strengths: List[str]
    weaknesses: List[str]
    career_suggestions: List[str]

class DISCReport(BaseModel):
    user_id: str
    test_type: str = "DISC"
    d_score: int  # Dominance
    i_score: int  # Influence
    s_score: int  # Steadiness
    c_score: int  # Conscientiousness
    primary_style: str  # e.g., "D", "I", "S", "C"
    secondary_style: Optional[str]
    description: str
    communication_style: str
    work_style: str

class Big5Report(BaseModel):
    user_id: str
    test_type: str = "Big5"
    openness: float  # 開放性
    conscientiousness: float  # 盡責性
    extraversion: float  # 外向性
    agreeableness: float  # 親和性
    neuroticism: float  # 神經質
    description: str
    personality_profile: str

class EnneagramReport(BaseModel):
    user_id: str
    test_type: str = "Enneagram"
    primary_type: int  # 1-9
    wing: Optional[int]  # 翼型
    tritype: Optional[List[int]]  # 三元組
    description: str
    core_fear: str
    core_desire: str
    growth_direction: str
    stress_direction: str

class CompositeReport(BaseModel):
    user_id: str
    test_type: str = "Composite"
    completed_tests: List[str]
    mbti_result: Optional[MBTIReport]
    disc_result: Optional[DISCReport]
    big5_result: Optional[Big5Report]
    enneagram_result: Optional[EnneagramReport]
    overall_analysis: str
    career_recommendations: List[str]
    personal_development_suggestions: List[str]
    compatibility_insights: Dict[str, Any] 
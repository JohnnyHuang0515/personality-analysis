from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class TestAnswer(Base):
    __tablename__ = 'test_answer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    question_id = Column(Integer, ForeignKey('test_question.id'), nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class TestQuestion(Base):
    __tablename__ = 'test_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    category = Column(String(32), nullable=False)
    test_type = Column(String(16), nullable=False)
    options = Column(Text, nullable=False)  # JSON 字串
    weight = Column(Text, nullable=False)   # JSON 字串 
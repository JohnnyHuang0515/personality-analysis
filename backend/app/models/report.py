from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class TestReport(Base):
    __tablename__ = 'test_report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    test_type = Column(String(16), nullable=False)
    result = Column(Text, nullable=False)  # JSON 字串
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
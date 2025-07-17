from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class TestSession(Base):
    __tablename__ = "test_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True)
    test_type = Column(String(32), index=True)  # MBTI, DISC, Big5, Enneagram, composite
    question_ids = Column(Text)  # JSON 陣列，存放本次測驗的題目 id
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(16), default="in_progress")  # in_progress, finished

class TestQuestion(Base):
    __tablename__ = "test_questions"
    id = Column(Integer, primary_key=True, index=True)
    test_type = Column(String(32), index=True)  # MBTI, DISC, Big5, Enneagram
    question_text = Column(Text, nullable=False)
    options = Column(Text)  # 存放 JSON 字串，內容為選項陣列

class TestAnswer(Base):
    __tablename__ = "test_answers"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"))
    user_id = Column(String(64), index=True)
    test_type = Column(String(32), index=True)
    question_id = Column(Integer, ForeignKey("test_questions.id"))
    answer = Column(String(128))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TestReport(Base):
    __tablename__ = "test_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), index=True)
    test_type = Column(String(32), index=True)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 資料庫 URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./personality_test.db"

# 建立 engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 需要這個設定
)

# 建立 SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base
Base = declarative_base()

# 依賴注入函數
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化資料庫函數
def init_db():
    """初始化資料庫，建立所有表格"""
    try:
        # 導入模型以確保表格被建立
        from app.models import TestQuestion, TestAnswer, TestReport
        # 建立所有表格
        Base.metadata.create_all(bind=engine)
        print("資料庫初始化成功")
    except Exception as e:
        print(f"資料庫初始化失敗: {e}") 
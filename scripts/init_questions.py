import os
import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.question import Base, TestQuestion

SQLALCHEMY_DATABASE_URL = "sqlite:///../backend/personality_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_TYPES = ["MBTI", "DISC", "Big5", "Enneagram"]

# 各測驗題目主題模板
QUESTION_TEMPLATES = {
    "MBTI": "在以下情境中，你會更傾向哪一種做法？",
    "DISC": "遇到這種情況時，你通常會怎麼反應？",
    "Big5": "你對下列描述的認同程度為何？",
    "Enneagram": "面對這種狀況，你的直覺選擇是？"
}

OPTION_TEMPLATES = [
    ["A. 積極參與社交活動", "B. 喜歡獨處並思考"],
    ["A. 立即採取行動", "B. 先觀察再決定"],
    ["A. 喜歡規劃未來", "B. 隨遇而安"],
    ["A. 重視感受", "B. 重視邏輯"],
    ["A. 喜歡團隊合作", "B. 偏好獨立完成"],
    ["A. 樂於接受新挑戰", "B. 喜歡穩定環境"],
    ["A. 直接表達意見", "B. 謹慎選擇言詞"],
    ["A. 喜歡嘗試新事物", "B. 偏好熟悉流程"],
    ["A. 注重細節", "B. 著重大方向"],
    ["A. 喜歡計畫", "B. 隨機應變"]
]

def generate_question(test_type, idx):
    template = QUESTION_TEMPLATES[test_type]
    option_pair = OPTION_TEMPLATES[idx % len(OPTION_TEMPLATES)]
    question_text = f"{template}（題號{idx+1}）"
    return TestQuestion(
        test_type=test_type,
        text=question_text,
        category=test_type,
        options=json.dumps(option_pair),
        weight=json.dumps({"A": {"score": 1}, "B": {"score": 1}})
    )

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for test_type in TEST_TYPES:
            # 檢查是否已經有資料
            exist_count = db.query(TestQuestion).filter(TestQuestion.test_type == test_type).count()
            if exist_count >= 50:
                print(f"{test_type} 已有 {exist_count} 題，略過初始化。")
                continue
            for i in range(50):
                q = generate_question(test_type, i)
                db.add(q)
            db.commit()
            print(f"{test_type} 題庫初始化完成，共 50 題。")
    finally:
        db.close()

if __name__ == "__main__":
    main() 
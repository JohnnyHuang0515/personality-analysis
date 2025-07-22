from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api import router as api_router

app = FastAPI(
    title="綜合人格特質分析 API",
    description="提供 MBTI、DISC、Big5、Enneagram 四種人格測驗的 API 服務",
    version="1.0.0"
)

# 加入 CORS 設定，允許前端開發伺服器請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "綜合人格特質分析後端啟動成功"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "服務正常運行"}
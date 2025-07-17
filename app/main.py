from fastapi import FastAPI
from app.core.database import init_db
from app.api import router as api_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "綜合人格特質分析後端啟動成功"} 
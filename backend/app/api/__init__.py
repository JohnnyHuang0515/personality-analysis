from fastapi import APIRouter
from app.api import questions, answers, reports, sessions

router = APIRouter()

# 包含所有 API 路由
router.include_router(questions.router, prefix="/api/v1", tags=["questions"])
router.include_router(answers.router, prefix="/api/v1", tags=["answers"])
router.include_router(reports.router, prefix="/api/v1", tags=["reports"])
router.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])

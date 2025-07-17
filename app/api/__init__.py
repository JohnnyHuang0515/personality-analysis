from fastapi import APIRouter
from app.api import questions, answers, sessions

router = APIRouter()
router.include_router(questions.router)
router.include_router(answers.router)
router.include_router(sessions.router) 
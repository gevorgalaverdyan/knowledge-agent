from fastapi import APIRouter

from app.api import chat, user


router = APIRouter()
router.include_router(chat.router)
router.include_router(user.router)

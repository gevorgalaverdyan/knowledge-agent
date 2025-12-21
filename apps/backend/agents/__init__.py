from fastapi import APIRouter

from api import chat


router = APIRouter()
router.include_router(chat.router)
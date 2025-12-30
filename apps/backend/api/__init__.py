from fastapi import APIRouter

from api import (chat, user)


router = APIRouter()
router.include_router(chat.router)
router.include_router(user.router)

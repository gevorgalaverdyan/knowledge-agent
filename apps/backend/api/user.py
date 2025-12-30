import logging
from fastapi import APIRouter, Depends

from core.config import get_settings
from core.auth import get_auth0
from core.db import SessionLocal


logger = logging.getLogger(__name__)

router = APIRouter(tags=["user"], prefix="/user")

settings = get_settings()
auth0 = get_auth0()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/profile", description="Fetch user profile information")
def get_user_profile(auth_result: dict = Depends(auth0.require_auth())):
    logger.info("Fetching user profile information.")
    return {"code": 200, "auth": auth_result}

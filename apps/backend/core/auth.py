from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.setup import configure_auth0
from models.user import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache(maxsize=1)
def get_auth0():
    """Return a singleton Auth0 client for the process.

    This avoids trying to import an `auth0` variable from `main.py` (which would
    create circular imports) while still sharing the same configured instance
    across routers.
    """

    return configure_auth0()


def get_current_user(
    auth_result: dict = Depends(get_auth0().require_auth()),
    db: Session = Depends(get_db),
):
    print(auth_result)
    auth0_id = auth_result.get("sub")

    user = db.query(User).filter(User.id == auth0_id).first()

    if not user:
        user = User(
            id=auth0_id,
            # email=auth_result.get("email"),
            # name=auth_result.get("name", "New User"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

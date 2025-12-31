from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import relationship
from core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, unique=True)
    # email = Column(String, unique=True, index=True, nullable=False)
    # name = Column(String, nullable=False)
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", back_populates="owner", cascade="all, delete-orphan")
from sqlalchemy import UUID, Column, DateTime, String, func
from sqlalchemy.orm import relationship
from core.db import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID, primary_key=True, index=True, default=func.uuid_generate_v4())
    chat_title = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )

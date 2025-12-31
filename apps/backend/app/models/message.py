import enum
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Text, func, Enum, text as sql_text
from sqlalchemy.orm import relationship
from app.core.db import Base


class MessageSenderType(enum.Enum):
    USER = "user"
    SYSTEM = "system"


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True, index=True, server_default=sql_text("uuid_generate_v4()"))
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    text = Column(Text, index=True, nullable=False)
    sent_by = Column(Enum(MessageSenderType), nullable=False)
    # pylint: disable=not-callable
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages")

import enum
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Text, func, Enum
from core.db import Base


class MessageSenderType(enum.Enum):
    USER = "user"
    SYSTEM = "system"


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True, index=True, default=func.uuid_generate_v4())
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    text = Column(Text, index=True, nullable=False)
    sent_by = Column(Enum(MessageSenderType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

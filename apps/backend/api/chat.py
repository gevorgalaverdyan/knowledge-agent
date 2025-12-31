import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.auth import get_auth0, get_current_user
from core.db import SessionLocal
from core.setup import retriever, client
from core.config import get_settings
from models.chat import Chat
from models.message import Message, MessageSenderType
from models.user import User
from rag.ask import ask_llm
from utils.utils import format_chat_history

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"], prefix="/chat")

settings = get_settings()
auth0 = get_auth0()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/chats", description="Fetch all chat sessions")
def get_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _ = Depends(auth0.require_auth())):
    chats = db.query(Chat).where(Chat.owner_id == current_user.id).all()
    return {"code": 200, "chats": chats}


@router.post("/create", description="Create a new chat session")
def create_chat(chat_title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _ = Depends(auth0.require_auth())):
    logger.info("Creating a new chat session.")
    chat = Chat(chat_title=chat_title, owner_id=current_user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {"code": 201, "chat": chat}

@router.delete("/{chat_id}/delete", description="Delete a chat session")
def delete_chat(chat_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), _ = Depends(auth0.require_auth())):
    logger.info("Deleting chat session with id: %s", chat_id)
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        logger.error("Chat with id %s not found.", chat_id)
        return {"code": 404, "error": "Chat not found."}

    db.delete(chat)
    db.commit()
    logger.info("Chat session with id %s deleted successfully.", chat_id)
    return {"code": 200, "message": "Chat deleted successfully."}

@router.get(
    "/{chat_id}/messages", description="Retrieve messages for a specific chat session"
)
def get_messages(chat_id: str, db: Session = Depends(get_db), _ = Depends(auth0.require_auth())):
    logger.info("Retrieving messages for chat_id: %s", chat_id)
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        logger.error("Chat with id %s not found.", chat_id)
        return {"code": 404, "error": "Chat not found."}

    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat.id)
        .order_by(Message.created_at)
        .all()
    )

    return {"code": 200, "chat_id": str(chat.id), "messages": messages}


@router.post(
    "/{chat_id}/message", description="Send a message to the chat and receive an answer"
)
def create_message(chat_id: str, question: str, db: Session = Depends(get_db), _ = Depends(auth0.require_auth())):
    logger.info("Received question: %s", question)

    if not question.strip():
        logger.warning("Empty question received.")
        return {"answer": "Please provide a valid question."}

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        logger.error("Chat with id %s not found.", chat_id)
        return {"code": 404, "error": "Chat not found."}

    message = Message(chat_id=chat.id, text=question, sent_by=MessageSenderType.USER)
    db.add(message)
    db.commit()
    db.refresh(message)

    chunks = retriever.search(question)
    if not chunks:
        logger.warning("No relevant CRA sections found.")
        message = Message(
            chat_id=chat.id,
            text="No relevant CRA sections found.",
            sent_by=MessageSenderType.SYSTEM,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return {"code": 204, "message": message}

    recent_messages = _get_recent_messages(chat_id, db)

    chat_history = format_chat_history(recent_messages)

    answer = ask_llm(
        chunks, question, client, settings.GEMINI_GENAI_MODEL, chat_history=chat_history
    )
    logger.info("Generated answer: %s", answer)

    if not answer:
        logger.warning("No answer could be generated.")
        answer = "No answer could be generated."

    message = Message(
        chat_id=chat.id,
        text=answer,
        sent_by=MessageSenderType.SYSTEM,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {"code": 200, "message": message}


def _get_recent_messages(chat_id: str, db: Session, limit: int = 5):
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

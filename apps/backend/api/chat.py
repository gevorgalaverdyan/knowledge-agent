import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.setup import retriever, client
from core.config import settings
from models.chat import Chat
from models.message import Message, MessageSenderType
from rag.ask import ask_llm

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"], prefix="/chat")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_chat(title: str, db: Session = Depends(get_db)):
    logger.info("Creating a new chat session.")
    chat = Chat(chat_title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return 201, {"chat_id": str(chat.id), "message": "Chat created successfully."}


@router.post("/message")
def create_message(chat_id: str, question: str, db: Session = Depends(get_db)):
    logger.info("Received question: %s", question)

    if not question.strip():
        logger.warning("Empty question received.")
        return {"answer": "Please provide a valid question."}

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        logger.error("Chat with id %s not found.", chat_id)
        return 404, {"error": "Chat not found."}

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
        return 204, {
            "message": {
                "id": str(message.id),
                "text": message.text,
                "sent_by": message.sent_by.value,
                "created_at": message.created_at,
            }
        }

    answer = ask_llm(chunks, question, client, settings.GENAI_MODEL)
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

    return 200, {
        "message": {
            "id": str(message.id),
            "text": answer,
            "sent_by": MessageSenderType.SYSTEM.value,
            "created_at": message.created_at,
        }
    }

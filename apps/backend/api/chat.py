from fastapi import APIRouter
from core.setup import retriever, client
from rag.ask import ask_llm
from core.config import settings
from schemas.chat import GeminiResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"], prefix="/chat")

@router.post("/")
def chat(question: str):
    logger.info(f"Received question: {question}")
    chunks = retriever.search(question)
    if not chunks:
        logger.warning("No relevant CRA sections found.")
        return {"answer": "No relevant CRA sections found."}

    answer = ask_llm(chunks, question, client, settings.GENAI_MODEL)
    logger.info(f"Generated answer: {answer}")
    
    if not answer:
        logger.warning("No answer could be generated.")
        answer = "No answer could be generated"
        
    return GeminiResponse(answer=answer)
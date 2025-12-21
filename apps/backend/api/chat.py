from fastapi import APIRouter
from core.setup import retriever, client
from rag.ask import ask_llm
from core.config import settings
from schemas.chat import GeminiResponse

router = APIRouter(tags=["chat"], prefix="/chat")

@router.post("/")
def chat(question: str):
    chunks = retriever.search(question)
    if not chunks:
        return {"answer": "No relevant CRA sections found."}

    answer = ask_llm(chunks, question, client, settings.GENAI_MODEL)

    if not answer:
        answer = "No answer could be generated"
        
    return GeminiResponse(answer=answer)
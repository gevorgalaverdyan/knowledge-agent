from fastapi import APIRouter, FastAPI

from llm.gemini import get_gemini_client
from rag.retriever import FaissRetriever

def create_app(router: APIRouter) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

client = get_gemini_client()

retriever = FaissRetriever(
    index_path="embedding/tfsa.faiss",
    metadata_path="embedding/tfsa_embeddings.json",
    client=client
)
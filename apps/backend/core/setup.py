import logging
import sys

from fastapi import APIRouter, FastAPI

from llm.gemini import get_gemini_client
from rag.retriever import FaissRetriever

def setup_logging(level=logging.INFO):
    """
    Configure application-wide logging.
    Call this ONCE at startup.
    """

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        root_logger.addHandler(handler)


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

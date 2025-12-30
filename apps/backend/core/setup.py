import logging
import sys

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_plugin.fast_api_client import Auth0FastAPI
from llm.gemini import get_gemini_client
from core.config import get_settings
from rag.retriever import FaissRetriever


def setup_logging(level=logging.INFO):
    """
    Configure application-wide logging.
    Call this ONCE at startup.
    """

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        root_logger.addHandler(handler)


def create_app(router: APIRouter, lifespan=None) -> FastAPI:
    origins = [
        "http://localhost",
        "http://localhost:4200",
    ]

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


def configure_auth0():
    settings = get_settings()

    auth0 = Auth0FastAPI(
        domain=settings.AUTH0_DOMAIN,
        audience=settings.AUTH0_AUDIENCE,
    )

    return auth0


client = get_gemini_client()

retriever = FaissRetriever(
    index_path="embedding/tfsa.faiss",
    metadata_path="embedding/tfsa_embeddings.json",
    client=client,
)

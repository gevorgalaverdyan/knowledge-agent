import logging
from contextlib import asynccontextmanager

from api import router
from core.auth import get_auth0
from core.db import Base, engine
from core.setup import create_app, setup_logging

setup_logging(logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    if engine.url.get_backend_name().startswith("postgres"):
        with engine.begin() as conn:
            conn.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    # Ensure required tables exist before handling requests
    Base.metadata.create_all(bind=engine)
    yield


app = create_app(router, lifespan=lifespan)
auth0 = get_auth0()

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Server is running"}

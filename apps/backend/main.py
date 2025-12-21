import logging
from api import router
from core.setup import create_app, setup_logging

setup_logging(logging.INFO)
logger = logging.getLogger(__name__)
app = create_app(router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Server is running"}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_settings

try:
    DATABASE_URL = get_settings().DB_URL
    if not DATABASE_URL:
        raise ValueError("DB_URL environment variable is not set.")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
except Exception as e:
    raise RuntimeError(f"Failed to set up database connection: {e}") from e

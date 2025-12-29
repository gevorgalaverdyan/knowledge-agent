import sys
import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Set environment variables required for imports
os.environ['DB_URL'] = 'sqlite:///:memory:'
os.environ['GEMINI_API_KEY'] = 'test-api-key-for-testing'

# Import and patch core.db before other imports
import core.db

# Create a test base
TestBase = declarative_base()
core.db.Base = TestBase

# Now import models so they use the TestBase
from models.chat import Chat as ChatModel
from models.message import Message
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    TestBase.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal
    
    # Cleanup
    TestBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Create a database session for testing."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with a test database."""
    from main import app
    from api.chat import get_db
    
    def override_get_db():
        session = test_db()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

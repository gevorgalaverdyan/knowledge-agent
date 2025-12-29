import sys
import os
import pytest
from unittest.mock import Mock, MagicMock

# Set test environment variables before importing modules
os.environ["DB_URL"] = "sqlite:///:memory:"

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client for testing"""
    client = Mock()
    response = Mock()
    response.text = "This is a mocked response from the LLM."
    client.models.generate_content.return_value = response
    return client

@pytest.fixture
def mock_retriever():
    """Mock FAISS retriever for testing"""
    retriever = Mock()
    retriever.search.return_value = [
        {
            "id": "test-1",
            "section": "Test Section 1",
            "topic": "Test Topic",
            "text": "This is test text from CRA.",
            "document": "CRA",
            "jurisdiction": "Canada",
            "year": 2025,
            "score": 0.95
        }
    ]
    return retriever

@pytest.fixture
def sample_chat_data():
    """Sample chat data for testing"""
    return {
        "chat_title": "Test Chat",
        "question": "What is my TFSA contribution room if I turned 18 in 2010?",
        "messages": [
            {"text": "Hello", "sent_by": "user"},
            {"text": "Hi there", "sent_by": "system"}
        ]
    }

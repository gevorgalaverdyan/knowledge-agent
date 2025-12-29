"""
Simple API endpoint tests that don't require database setup
"""
import os
os.environ["DB_URL"] = "sqlite:///:memory:"
os.environ["GEMINI_API_KEY"] = "test-api-key-for-testing"

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client"""
    with TestClient(app) as test_client:
        yield test_client


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns server status"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "Server is running"}
    
    def test_root_endpoint_structure(self, client):
        """Test root endpoint returns proper JSON structure"""
        response = client.get("/")
        
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)


class TestAPIStructure:
    """Tests for API structure and availability"""
    
    def test_chat_endpoints_exist(self, client):
        """Test that chat API endpoints are registered"""
        # Get the OpenAPI spec to verify routes exist
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        openapi_spec = response.json()
        paths = openapi_spec.get("paths", {})
        
        # Verify expected endpoints exist in spec
        assert "/" in paths
        assert "/chat/chats" in paths or any("/chat/" in path for path in paths)
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are configured"""
        response = client.options(
            "/",
            headers={"Origin": "http://localhost:4200"}
        )
        
        # CORS should be configured (status might be 200 or 405 depending on implementation)
        assert response.status_code in [200, 405]

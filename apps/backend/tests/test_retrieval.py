"""
Unit tests for retrieval tools in tools/retrieval.py
"""
import os
os.environ["DB_URL"] = "sqlite:///:memory:"
os.environ["GEMINI_API_KEY"] = "test-api-key-for-testing"

import pytest
from unittest.mock import Mock, patch
from tools.retrieval import find_relevant_sections
from schemas.chat import Section


class TestFindRelevantSections:
    """Tests for find_relevant_sections function"""
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_returns_sections(self, mock_retriever):
        """Test that function returns Section objects"""
        mock_retriever.search.return_value = [
            {
                "id": "section-1",
                "section": "Eligibility",
                "topic": "TFSA Basics",
                "text": "You must be 18 or older.",
                "document": "CRA",
                "jurisdiction": "Canada",
                "year": 2025,
                "score": 0.95
            },
            {
                "id": "section-2",
                "section": "Contributions",
                "topic": "TFSA Limits",
                "text": "Annual contribution limits apply.",
                "document": "CRA",
                "jurisdiction": "Canada",
                "year": 2025,
                "score": 0.90
            }
        ]
        
        query = "What are TFSA eligibility requirements?"
        sections = find_relevant_sections(query)
        
        assert len(sections) == 2
        assert all(isinstance(section, Section) for section in sections)
        assert sections[0].id == "section-1"
        assert sections[0].section == "Eligibility"
        assert sections[1].id == "section-2"
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_with_custom_top_k(self, mock_retriever):
        """Test that top_k parameter is passed to retriever"""
        mock_retriever.search.return_value = []
        
        query = "Test query"
        find_relevant_sections(query, top_k=3)
        
        mock_retriever.search.assert_called_once_with(query, 3)
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_default_top_k(self, mock_retriever):
        """Test that default top_k is 5"""
        mock_retriever.search.return_value = []
        
        query = "Test query"
        find_relevant_sections(query)
        
        mock_retriever.search.assert_called_once_with(query, 5)
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_empty_results(self, mock_retriever):
        """Test handling of empty search results"""
        mock_retriever.search.return_value = []
        
        query = "Test query"
        sections = find_relevant_sections(query)
        
        assert len(sections) == 0
        assert sections == []
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_with_missing_optional_fields(self, mock_retriever):
        """Test handling of results with missing optional fields"""
        mock_retriever.search.return_value = [
            {
                "id": "section-1",
                "section": "Test Section",
                "text": "Test content.",
                # Missing optional fields like topic, document, jurisdiction, year
            }
        ]
        
        query = "Test query"
        sections = find_relevant_sections(query)
        
        assert len(sections) == 1
        assert sections[0].id == "section-1"
        assert sections[0].topic == ""
        assert sections[0].document == "CRA"
        assert sections[0].jurisdiction == "Canada"
        assert sections[0].year == 2025
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_preserves_all_fields(self, mock_retriever):
        """Test that all fields are correctly mapped to Section objects"""
        mock_retriever.search.return_value = [
            {
                "id": "test-123",
                "section": "Test Section Name",
                "topic": "Test Topic Name",
                "text": "This is the full text content.",
                "document": "CRA Guide",
                "jurisdiction": "Federal",
                "year": 2024,
                "score": 0.85
            }
        ]
        
        query = "Test query"
        sections = find_relevant_sections(query)
        
        section = sections[0]
        assert section.id == "test-123"
        assert section.section == "Test Section Name"
        assert section.topic == "Test Topic Name"
        assert section.text == "This is the full text content."
        assert section.document == "CRA Guide"
        assert section.jurisdiction == "Federal"
        assert section.year == 2024
    
    @patch('tools.retrieval.retriever')
    def test_find_relevant_sections_contribution_query(self, mock_retriever):
        """Test with a realistic contribution room query"""
        mock_retriever.search.return_value = [
            {
                "id": "contrib-1",
                "section": "Annual Contribution Limits",
                "topic": "TFSA Contribution Room",
                "text": "The TFSA contribution room is cumulative.",
                "document": "CRA",
                "jurisdiction": "Canada",
                "year": 2025
            }
        ]
        
        query = "What is my TFSA contribution room?"
        sections = find_relevant_sections(query, top_k=1)
        
        assert len(sections) == 1
        assert "contribution" in sections[0].text.lower() or "contribution" in sections[0].section.lower()
        mock_retriever.search.assert_called_once_with(query, 1)

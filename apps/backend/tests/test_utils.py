import pytest
from utils.utils import extract_year, format_chat_history, chunk_text
from models.message import MessageSenderType


class TestExtractYear:
    """Test cases for extract_year function."""

    def test_extract_year_with_valid_year(self):
        """Should extract year from question."""
        question = "I turned 18 in 2015"
        assert extract_year(question) == 2015

    def test_extract_year_with_year_in_sentence(self):
        """Should extract year from middle of sentence."""
        question = "What is my contribution room if I turned 18 in 2020?"
        assert extract_year(question) == 2020

    def test_extract_year_no_year(self):
        """Should return -1 when no year is found."""
        question = "What is my contribution room?"
        assert extract_year(question) == -1

    def test_extract_year_only_extracts_2000s(self):
        """Should only extract years in 20XX format."""
        question = "I was born in 1999 and turned 18 in 2017"
        assert extract_year(question) == 2017


class TestFormatChatHistory:
    """Test cases for format_chat_history function."""

    def test_format_empty_history(self):
        """Should return empty string for empty history."""
        messages = []
        assert format_chat_history(messages) == ""

    def test_format_single_user_message(self):
        """Should format single user message correctly."""
        class MockMessage:
            def __init__(self, text, sent_by):
                self.text = text
                self.sent_by = sent_by
        
        messages = [MockMessage("Hello", "user")]
        result = format_chat_history(messages)
        assert result == "User: Hello"

    def test_format_multiple_messages(self):
        """Should format multiple messages correctly."""
        class MockMessage:
            def __init__(self, text, sent_by):
                self.text = text
                self.sent_by = sent_by
        
        messages = [
            MockMessage("Hello", "user"),
            MockMessage("Hi there!", "system"),
            MockMessage("How are you?", "user")
        ]
        result = format_chat_history(messages)
        expected = "User: Hello\nAssistant: Hi there!\nUser: How are you?"
        assert result == expected


class TestChunkText:
    """Test cases for chunk_text function."""

    def test_chunk_text_with_sections(self):
        """Should correctly chunk text with section markers."""
        text = "[Section 1.1]Content for section 1.1[Section 1.2]Content for section 1.2"
        chunks = chunk_text(text)
        
        assert len(chunks) == 2
        assert chunks[0]["section"] == "Section 1.1"
        assert chunks[0]["text"] == "Content for section 1.1"
        assert chunks[1]["section"] == "Section 1.2"
        assert chunks[1]["text"] == "Content for section 1.2"

    def test_chunk_text_empty_string(self):
        """Should return empty list for empty string."""
        text = ""
        chunks = chunk_text(text)
        assert chunks == []

    def test_chunk_text_with_whitespace(self):
        """Should handle whitespace correctly."""
        text = "[Section 1]  Content with spaces  [Section 2]  More content  "
        chunks = chunk_text(text)
        
        assert len(chunks) == 2
        assert chunks[0]["section"] == "Section 1"
        assert chunks[0]["text"] == "Content with spaces"
        assert chunks[1]["section"] == "Section 2"
        assert chunks[1]["text"] == "More content"

    def test_chunk_text_single_section(self):
        """Should handle single section correctly."""
        text = "[Introduction]This is the introduction text."
        chunks = chunk_text(text)
        
        assert len(chunks) == 1
        assert chunks[0]["section"] == "Introduction"
        assert chunks[0]["text"] == "This is the introduction text."

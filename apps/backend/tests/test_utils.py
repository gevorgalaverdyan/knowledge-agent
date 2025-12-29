"""
Unit tests for utility functions in utils/utils.py
"""
import pytest
from utils.utils import chunk_text, extract_year, format_chat_history
from models.message import Message, MessageSenderType


class TestChunkText:
    """Tests for chunk_text function"""
    
    def test_chunk_text_with_valid_input(self):
        """Test chunking text with valid section format"""
        text = "[Section 1]This is content for section 1.[Section 2]This is content for section 2."
        chunks = chunk_text(text)
        
        assert len(chunks) == 2
        assert chunks[0]["section"] == "Section 1"
        assert chunks[0]["text"] == "This is content for section 1."
        assert chunks[1]["section"] == "Section 2"
        assert chunks[1]["text"] == "This is content for section 2."
    
    def test_chunk_text_with_empty_sections(self):
        """Test chunking text with empty content"""
        text = "[Section 1][Section 2]Some content."
        chunks = chunk_text(text)
        
        # Empty sections should be skipped
        assert len(chunks) == 1
        assert chunks[0]["section"] == "Section 2"
        assert chunks[0]["text"] == "Some content."
    
    def test_chunk_text_with_no_sections(self):
        """Test chunking text with no section markers"""
        text = "Just plain text without sections."
        chunks = chunk_text(text)
        
        assert len(chunks) == 0
    
    def test_chunk_text_with_whitespace(self):
        """Test chunking text with extra whitespace"""
        text = "[  Section 1  ]  Content with whitespace.  "
        chunks = chunk_text(text)
        
        assert len(chunks) == 1
        assert chunks[0]["section"] == "Section 1"
        assert chunks[0]["text"] == "Content with whitespace."


class TestExtractYear:
    """Tests for extract_year function"""
    
    def test_extract_year_valid_2000s(self):
        """Test extracting year from 2000s"""
        question = "I turned 18 in 2010, what is my contribution room?"
        year = extract_year(question)
        assert year == 2010
    
    def test_extract_year_valid_2020s(self):
        """Test extracting year from 2020s"""
        question = "My contribution room for 2023?"
        year = extract_year(question)
        assert year == 2023
    
    def test_extract_year_no_year(self):
        """Test extraction when no year is present"""
        question = "What is my TFSA contribution room?"
        year = extract_year(question)
        assert year == -1
    
    def test_extract_year_invalid_format(self):
        """Test extraction with invalid year format"""
        question = "I turned 18 in 1999"
        year = extract_year(question)
        assert year == -1
    
    def test_extract_year_multiple_years(self):
        """Test extraction with multiple years (should return first)"""
        question = "From 2010 to 2023, what is my total?"
        year = extract_year(question)
        assert year == 2010


class TestFormatChatHistory:
    """Tests for format_chat_history function"""
    
    def test_format_chat_history_empty(self):
        """Test formatting empty chat history"""
        messages = []
        formatted = format_chat_history(messages)
        assert formatted == ""
    
    def test_format_chat_history_single_message(self):
        """Test formatting single message"""
        message = type('Message', (), {
            'text': 'Hello',
            'sent_by': 'user'
        })()
        messages = [message]
        formatted = format_chat_history(messages)
        assert formatted == "User: Hello"
    
    def test_format_chat_history_multiple_messages(self):
        """Test formatting multiple messages"""
        message1 = type('Message', (), {
            'text': 'Hello',
            'sent_by': 'user'
        })()
        message2 = type('Message', (), {
            'text': 'Hi there',
            'sent_by': 'system'
        })()
        message3 = type('Message', (), {
            'text': 'How can I help?',
            'sent_by': 'user'
        })()
        
        messages = [message1, message2, message3]
        formatted = format_chat_history(messages)
        
        expected = "User: Hello\nAssistant: Hi there\nUser: How can I help?"
        assert formatted == expected
    
    def test_format_chat_history_system_messages(self):
        """Test formatting with system messages"""
        message1 = type('Message', (), {
            'text': 'System message',
            'sent_by': 'system'
        })()
        
        messages = [message1]
        formatted = format_chat_history(messages)
        assert formatted == "Assistant: System message"

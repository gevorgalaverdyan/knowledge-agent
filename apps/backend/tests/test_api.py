import pytest
import uuid
from unittest.mock import patch, Mock
from models.chat import Chat as ChatModel
from models.message import Message, MessageSenderType


class TestChatAPI:
    """Integration tests for chat API endpoints."""

    def test_get_chats_empty(self, client, db_session):
        """Should return empty list when no chats exist."""
        response = client.get("/chat/chats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["chats"] == []

    def test_get_chats_with_data(self, client, db_session):
        """Should return all chats."""
        # Create test chats with explicit UUIDs for SQLite
        chat1 = ChatModel(id=uuid.uuid4(), chat_title="Chat 1")
        chat2 = ChatModel(id=uuid.uuid4(), chat_title="Chat 2")
        db_session.add(chat1)
        db_session.add(chat2)
        db_session.commit()
        
        response = client.get("/chat/chats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["chats"]) == 2

    def test_get_messages_chat_not_found(self, client):
        """Should return 404 when chat doesn't exist."""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/chat/{fake_id}/messages")
        
        data = response.json()
        assert data["code"] == 404
        assert "not found" in data["error"].lower()

    def test_get_messages_empty(self, client, db_session):
        """Should return empty messages for new chat."""
        chat = ChatModel(id=uuid.uuid4(), chat_title="Test Chat")
        db_session.add(chat)
        db_session.commit()
        db_session.refresh(chat)
        
        response = client.get(f"/chat/{chat.id}/messages")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["messages"] == []

    def test_get_messages_with_data(self, client, db_session):
        """Should return messages for chat."""
        chat = ChatModel(id=uuid.uuid4(), chat_title="Test Chat")
        db_session.add(chat)
        db_session.commit()
        db_session.refresh(chat)
        
        # Add messages with explicit UUIDs
        msg1 = Message(id=uuid.uuid4(), chat_id=chat.id, text="Hello", sent_by=MessageSenderType.USER)
        msg2 = Message(id=uuid.uuid4(), chat_id=chat.id, text="Hi there", sent_by=MessageSenderType.SYSTEM)
        db_session.add(msg1)
        db_session.add(msg2)
        db_session.commit()
        
        response = client.get(f"/chat/{chat.id}/messages")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["messages"]) == 2

    def test_create_message_empty_question(self, client, db_session):
        """Should handle empty question."""
        chat = ChatModel(id=uuid.uuid4(), chat_title="Test Chat")
        db_session.add(chat)
        db_session.commit()
        db_session.refresh(chat)
        
        response = client.post(f"/chat/{chat.id}/message?question=   ")
        
        data = response.json()
        assert "valid question" in data["answer"].lower()

    @patch('api.chat.retriever')
    def test_create_message_no_chunks_found(self, mock_retriever, client, db_session):
        """Should handle when no relevant sections are found."""
        chat = ChatModel(id=uuid.uuid4(), chat_title="Test Chat")
        db_session.add(chat)
        db_session.commit()
        db_session.refresh(chat)
        
        mock_retriever.search.return_value = []
        
        response = client.post(f"/chat/{chat.id}/message?question=Random question")
        
        data = response.json()
        assert data["code"] == 204

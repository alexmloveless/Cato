"""
Integration tests for chat service.

Tests cover:
- Chat service initialization
- Message sending and receiving
- Conversation history management
- Context truncation
- Retry logic
- Thread continuation
"""

import pytest

from cato.services.chat import ChatService
from cato.services.conversation import Conversation
from cato.core.types import Message


@pytest.mark.asyncio
class TestChatService:
    """Test chat service functionality."""

    async def test_chat_initialization(self, mock_llm, test_config):
        """Test initializing chat service."""
        service = ChatService(
            provider=mock_llm,
            config=test_config,
            system_prompt="You are a helpful assistant.",
        )

        assert service.provider == mock_llm
        assert service.config == test_config
        assert service.session_id is not None
        assert service.conversation is not None

    async def test_send_message(self, mock_llm, test_config):
        """Test sending a message and getting response."""
        mock_llm.set_response("Hello! How can I help you?")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
            system_prompt="You are helpful.",
        )

        result = await service.send_message("Hi there!")

        assert result.content == "Hello! How can I help you?"
        assert result.model == "mock-model"
        assert mock_llm.call_count == 1

    async def test_conversation_history(self, mock_llm, test_config):
        """Test that conversation history is maintained."""
        mock_llm.set_responses([
            "Response 1",
            "Response 2",
        ])

        service = ChatService(
            provider=mock_llm,
            config=test_config,
            system_prompt="You are helpful.",
        )

        await service.send_message("Message 1")
        await service.send_message("Message 2")

        # Check message count
        assert service.get_message_count() == 4  # 2 user + 2 assistant

        # Verify history includes all messages
        messages = service.conversation.to_messages()
        user_messages = [m for m in messages if m.role == "user"]
        assert len(user_messages) == 2

    async def test_clear_conversation(self, mock_llm, test_config):
        """Test clearing conversation history."""
        mock_llm.set_response("Response")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
            system_prompt="System prompt",
        )

        await service.send_message("Test message")
        assert service.get_message_count() > 0

        service.clear_conversation()
        assert service.get_message_count() == 0

        # System prompt should be preserved
        messages = service.conversation.to_messages()
        assert any(m.role == "system" for m in messages)

    async def test_update_system_prompt(self, mock_llm, test_config):
        """Test updating system prompt."""
        service = ChatService(
            provider=mock_llm,
            config=test_config,
            system_prompt="Original prompt",
        )

        service.update_system_prompt("New prompt")

        messages = service.conversation.to_messages()
        system_messages = [m for m in messages if m.role == "system"]
        assert system_messages[0].content == "New prompt"

    async def test_temperature_override(self, mock_llm, test_config):
        """Test overriding temperature parameter."""
        mock_llm.set_response("Response")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
        )

        await service.send_message("Test", temperature=0.9)

        # Check that temperature was passed to provider
        call = mock_llm.calls[0]
        assert call["temperature"] == 0.9

    async def test_max_tokens_override(self, mock_llm, test_config):
        """Test overriding max_tokens parameter."""
        mock_llm.set_response("Response")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
        )

        await service.send_message("Test", max_tokens=1000)

        # Check that max_tokens was passed to provider
        call = mock_llm.calls[0]
        assert call["max_tokens"] == 1000


@pytest.mark.asyncio
class TestChatWithVectorStore:
    """Test chat service with vector store integration."""

    async def test_store_exchange(self, mock_llm, mock_vector_store, test_config):
        """Test storing conversation exchanges in vector store."""
        mock_llm.set_response("Answer to your question")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
            vector_store=mock_vector_store,
        )

        await service.send_message("What is the answer?")

        # Verify exchange was stored
        count = await mock_vector_store.count()
        assert count == 1

    async def test_retrieve_context(self, mock_llm, mock_vector_store, test_config):
        """Test retrieving context from vector store."""
        # Pre-populate vector store
        from cato.storage.vector.base import VectorDocument
        await mock_vector_store.add([
            VectorDocument(
                id="ctx-1",
                content="User: Previous question\n\nAssistant: Previous answer",
                metadata={"type": "exchange"},
            )
        ])

        mock_llm.set_response("New response")

        service = ChatService(
            provider=mock_llm,
            config=test_config,
            vector_store=mock_vector_store,
        )

        # Send message with similar content
        await service.send_message("question")

        # LLM should have been called
        assert mock_llm.call_count == 1

    async def test_continue_thread(self, mock_llm, mock_vector_store, test_config):
        """Test continuing a previous thread."""
        from cato.storage.vector.base import VectorDocument
        import uuid

        # Create a previous session with exchanges
        session_id = str(uuid.uuid4())[:8]

        await mock_vector_store.add([
            VectorDocument(
                id="ex-1",
                content="User: First message\n\nAssistant: First response",
                metadata={
                    "type": "exchange",
                    "session_id": session_id,
                    "timestamp": "2024-01-01T10:00:00",
                },
            ),
            VectorDocument(
                id="ex-2",
                content="User: Second message\n\nAssistant: Second response",
                metadata={
                    "type": "exchange",
                    "session_id": session_id,
                    "timestamp": "2024-01-01T10:01:00",
                },
            ),
        ])

        # Create service and continue thread
        service = ChatService(
            provider=mock_llm,
            config=test_config,
            vector_store=mock_vector_store,
        )

        count = await service.continue_thread(session_id)

        assert count == 2
        assert service.get_message_count() == 4  # 2 exchanges = 4 messages
        assert service.session_id == session_id


@pytest.mark.asyncio
class TestConversation:
    """Test conversation management."""

    def test_create_conversation(self):
        """Test creating a conversation."""
        conv = Conversation(system_prompt="You are helpful")

        assert conv.system_prompt == "You are helpful"
        assert conv.message_count() == 0

    def test_add_messages(self):
        """Test adding messages to conversation."""
        conv = Conversation(system_prompt="System")

        conv.add_user_message("Hello")
        conv.add_assistant_message("Hi there!")

        assert conv.message_count() == 2

    def test_to_messages(self):
        """Test converting conversation to message list."""
        conv = Conversation(system_prompt="System prompt")

        conv.add_user_message("User message")
        conv.add_assistant_message("Assistant message")

        messages = conv.to_messages()

        assert len(messages) == 3  # system + user + assistant
        assert messages[0].role == "system"
        assert messages[1].role == "user"
        assert messages[2].role == "assistant"

    def test_clear_conversation(self):
        """Test clearing conversation."""
        conv = Conversation(system_prompt="System")

        conv.add_user_message("Message 1")
        conv.add_assistant_message("Response 1")

        assert conv.message_count() == 2

        conv.clear()

        assert conv.message_count() == 0
        # System prompt should still exist in to_messages()
        messages = conv.to_messages()
        assert any(m.role == "system" for m in messages)

    def test_truncate_to_tokens(self):
        """Test truncating conversation to fit token limit."""
        conv = Conversation(system_prompt="System prompt")

        # Add many messages
        for i in range(10):
            conv.add_user_message(f"Message {i}" * 100)  # Long messages
            conv.add_assistant_message(f"Response {i}" * 100)

        # Mock token counter (4 chars per token)
        def count_tokens(text):
            return len(text) // 4

        # Truncate to small limit
        conv.truncate_to_tokens(500, count_tokens)

        # Should have fewer messages now
        assert conv.message_count() < 20

    def test_truncate_preserves_recent_messages(self):
        """Test that truncation keeps most recent messages."""
        conv = Conversation(system_prompt="System")

        conv.add_user_message("Old message 1")
        conv.add_assistant_message("Old response 1")
        conv.add_user_message("Old message 2")
        conv.add_assistant_message("Old response 2")
        conv.add_user_message("Recent message")
        conv.add_assistant_message("Recent response")

        def count_tokens(text):
            return len(text) // 4

        # Truncate to very small limit
        conv.truncate_to_tokens(100, count_tokens)

        messages = conv.to_messages()
        # Most recent messages should be preserved
        assert any("Recent" in m.content for m in messages)

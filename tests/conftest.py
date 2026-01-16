"""
Shared pytest fixtures for Cato test suite.

This module provides fixtures for:
- Temporary database connections
- Mock LLM providers
- Mock vector stores
- Test configurations
- Temporary directories
"""

import asyncio
import tempfile
from pathlib import Path
from typing import AsyncIterator
from unittest.mock import AsyncMock, Mock

import pytest
import aiosqlite

from cato.core.config import CatoConfig, LLMConfig, VectorStoreConfig, StorageConfig
from cato.core.types import CompletionResult, Message, TokenUsage
from cato.providers.llm.base import LLMProvider
from cato.storage.database import Database
from cato.storage.vector.base import VectorStore, VectorDocument, SearchResult


# ============================================================================
# Event Loop Configuration
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Temporary Resources
# ============================================================================

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_db_path(temp_dir):
    """Provide a temporary database file path."""
    return temp_dir / "test.db"


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture
async def test_db(temp_db_path):
    """
    Provide a test database with schema initialized.

    Yields
    ------
    Database
        Connected database instance with all migrations applied.
    """
    db = Database(str(temp_db_path))
    await db.connect()

    # Run migrations to create schema
    from cato.storage.migrations import MIGRATIONS

    # Check if migrations table exists
    cursor = await db._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'"
    )
    table_exists = await cursor.fetchone()

    if not table_exists:
        await db._conn.execute(
            """
            CREATE TABLE migrations (
                id INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    # Apply all migrations
    for migration in MIGRATIONS:
        # Check if already applied
        cursor = await db._conn.execute(
            "SELECT id FROM migrations WHERE id = ?", (migration.id,)
        )
        applied = await cursor.fetchone()

        if not applied:
            await db._conn.executescript(migration.sql)
            await db._conn.execute(
                "INSERT INTO migrations (id) VALUES (?)", (migration.id,)
            )
            await db._conn.commit()

    yield db

    await db.close()


# ============================================================================
# Mock LLM Provider
# ============================================================================

class MockLLMProvider:
    """
    Mock LLM provider for testing.

    Provides configurable responses and tracks all calls.
    """

    def __init__(self):
        self._responses = []
        self._call_count = 0
        self._calls = []
        self.name = "mock"
        self.model = "mock-model"

    def set_response(self, content: str) -> None:
        """Set the next response to return."""
        self._responses.append(content)

    def set_responses(self, responses: list[str]) -> None:
        """Set multiple responses in order."""
        self._responses.extend(responses)

    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """Mock completion that returns pre-configured response."""
        self._call_count += 1
        self._calls.append({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        })

        if self._responses:
            content = self._responses.pop(0)
        else:
            content = f"Mock response {self._call_count}"

        return CompletionResult(
            content=content,
            model=self.model,
            usage=TokenUsage(
                prompt_tokens=100,
                completion_tokens=50,
                total_tokens=150,
            ),
        )

    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Mock streaming that yields response in chunks."""
        result = await self.complete(messages, temperature=temperature, max_tokens=max_tokens)
        # Yield in chunks
        words = result.content.split()
        for word in words:
            yield word + " "

    def count_tokens(self, text: str) -> int:
        """Mock token counter (4 chars per token)."""
        return len(text) // 4

    @property
    def call_count(self) -> int:
        """Number of times complete was called."""
        return self._call_count

    @property
    def calls(self) -> list[dict]:
        """List of all calls made."""
        return self._calls


@pytest.fixture
def mock_llm():
    """Provide a mock LLM provider."""
    return MockLLMProvider()


# ============================================================================
# Mock Vector Store
# ============================================================================

class MockVectorStore:
    """
    Mock vector store for testing.

    Stores documents in memory and provides simple search.
    """

    def __init__(self):
        self._documents: dict[str, VectorDocument] = {}

    async def add(self, documents: list[VectorDocument]) -> list[str]:
        """Add documents to the mock store."""
        ids = []
        for doc in documents:
            self._documents[doc.id] = doc
            ids.append(doc.id)
        return ids

    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter: dict | None = None,
    ) -> list[SearchResult]:
        """Mock search that returns all matching documents."""
        results = []

        for doc in self._documents.values():
            # Apply filter if provided
            if filter:
                match = all(
                    doc.metadata.get(k) == v
                    for k, v in filter.items()
                )
                if not match:
                    continue

            # Simple keyword matching
            if query.lower() in doc.content.lower():
                results.append(SearchResult(
                    document=doc,
                    score=0.5,  # Mock score
                ))

        return results[:n_results]

    async def get(self, ids: list[str]) -> list[VectorDocument]:
        """Retrieve documents by ID."""
        return [self._documents[id] for id in ids if id in self._documents]

    async def delete(self, ids: list[str]) -> None:
        """Delete documents by ID."""
        for id in ids:
            self._documents.pop(id, None)

    async def count(self) -> int:
        """Return document count."""
        return len(self._documents)


@pytest.fixture
def mock_vector_store():
    """Provide a mock vector store."""
    return MockVectorStore()


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def test_config(temp_dir):
    """
    Provide a test configuration with safe defaults.

    Uses temporary paths and disabled external services.
    """
    return CatoConfig(
        llm=LLMConfig(
            provider="mock",
            model="mock-model",
            temperature=0.7,
            max_tokens=2000,
        ),
        storage=StorageConfig(
            database_path=str(temp_dir / "test.db"),
        ),
        vector_store=VectorStoreConfig(
            enabled=False,
            type="chromadb",
            path=str(temp_dir / "chroma"),
        ),
    )


@pytest.fixture
def minimal_config():
    """Provide minimal valid configuration for testing."""
    return CatoConfig()


# ============================================================================
# Message Fixtures
# ============================================================================

@pytest.fixture
def sample_messages():
    """Provide sample conversation messages."""
    return [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Hello!"),
        Message(role="assistant", content="Hi! How can I help you?"),
        Message(role="user", content="What is 2+2?"),
    ]


# ============================================================================
# Async Utilities
# ============================================================================

@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"

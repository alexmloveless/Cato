"""
Integration tests for vector store operations.

Tests cover:
- Document storage and retrieval
- Similarity search
- Metadata filtering
"""

import pytest

from cato.storage.vector.base import VectorDocument


@pytest.mark.asyncio
class TestVectorStoreOperations:
    """Test vector store functionality with mock implementation."""

    async def test_add_documents(self, mock_vector_store):
        """Test adding documents to vector store."""
        docs = [
            VectorDocument(
                id="doc-1",
                content="Python is a programming language",
                metadata={"type": "definition"},
            ),
            VectorDocument(
                id="doc-2",
                content="JavaScript is used for web development",
                metadata={"type": "definition"},
            ),
        ]

        ids = await mock_vector_store.add(docs)

        assert len(ids) == 2
        assert "doc-1" in ids
        assert "doc-2" in ids

    async def test_search_documents(self, mock_vector_store):
        """Test searching for similar documents."""
        # Add documents
        docs = [
            VectorDocument(
                id="doc-1",
                content="The quick brown fox jumps",
                metadata={"type": "text"},
            ),
            VectorDocument(
                id="doc-2",
                content="The lazy dog sleeps",
                metadata={"type": "text"},
            ),
        ]
        await mock_vector_store.add(docs)

        # Search
        results = await mock_vector_store.search("fox", n_results=5)

        assert len(results) >= 1
        # Should find doc-1
        assert any(r.document.id == "doc-1" for r in results)

    async def test_get_by_id(self, mock_vector_store):
        """Test retrieving documents by ID."""
        doc = VectorDocument(
            id="get-test",
            content="Test content",
            metadata={},
        )
        await mock_vector_store.add([doc])

        # Retrieve
        retrieved = await mock_vector_store.get(["get-test"])

        assert len(retrieved) == 1
        assert retrieved[0].id == "get-test"
        assert retrieved[0].content == "Test content"

    async def test_delete_documents(self, mock_vector_store):
        """Test deleting documents."""
        doc = VectorDocument(
            id="delete-test",
            content="To be deleted",
            metadata={},
        )
        await mock_vector_store.add([doc])

        # Verify it exists
        assert await mock_vector_store.count() >= 1

        # Delete
        await mock_vector_store.delete(["delete-test"])

        # Try to retrieve
        retrieved = await mock_vector_store.get(["delete-test"])
        assert len(retrieved) == 0

    async def test_count_documents(self, mock_vector_store):
        """Test counting documents in store."""
        initial_count = await mock_vector_store.count()

        # Add documents
        docs = [
            VectorDocument(id=f"count-{i}", content=f"Content {i}", metadata={})
            for i in range(3)
        ]
        await mock_vector_store.add(docs)

        # Count should increase
        new_count = await mock_vector_store.count()
        assert new_count == initial_count + 3

    async def test_filter_by_metadata(self, mock_vector_store):
        """Test filtering search results by metadata."""
        # Add documents with different types
        docs = [
            VectorDocument(
                id="chat-1",
                content="User question about Python",
                metadata={"type": "exchange", "language": "python"},
            ),
            VectorDocument(
                id="doc-1",
                content="Python documentation",
                metadata={"type": "document", "language": "python"},
            ),
        ]
        await mock_vector_store.add(docs)

        # Search with filter
        results = await mock_vector_store.search(
            "Python",
            n_results=10,
            filter={"type": "exchange"},
        )

        # Should only get exchange type
        for result in results:
            if result.document.id in ["chat-1", "doc-1"]:
                assert result.document.metadata["type"] == "exchange"

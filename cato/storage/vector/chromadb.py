"""ChromaDB vector store implementation."""

import logging

import chromadb
from chromadb.config import Settings

from cato.core.exceptions import VectorStoreError, VectorStoreConnectionError
from cato.storage.embedding.base import EmbeddingProvider
from cato.storage.vector.base import VectorDocument, SearchResult

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """
    ChromaDB-backed vector store implementation.
    
    Uses persistent ChromaDB for semantic search over documents and conversation history.
    
    Parameters
    ----------
    path : str
        Path to persistent ChromaDB storage directory.
    collection_name : str
        Name of the ChromaDB collection to use.
    embedding_provider : EmbeddingProvider
        Provider for generating embeddings.
    """
    
    def __init__(
        self,
        path: str,
        collection_name: str,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._collection_name = collection_name
        
        try:
            # Initialize persistent ChromaDB client
            self._client = chromadb.PersistentClient(
                path=path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=False,
                ),
            )
            
            # Get or create collection with cosine similarity
            self._collection = self._client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            
            logger.info(
                f"ChromaDB vector store initialized: path={path}, "
                f"collection={collection_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise VectorStoreConnectionError(f"Failed to connect to ChromaDB: {e}") from e
    
    async def add(
        self,
        documents: list[VectorDocument],
    ) -> list[str]:
        """
        Add documents to the store.
        
        Parameters
        ----------
        documents : list[VectorDocument]
            Documents to add. Embeddings generated if not provided.
        
        Returns
        -------
        list[str]
            IDs of added documents.
        
        Raises
        ------
        VectorStoreError
            If adding documents fails.
        """
        try:
            # Generate embeddings for documents without them
            texts_to_embed = [
                (i, doc.content)
                for i, doc in enumerate(documents)
                if doc.embedding is None
            ]
            
            if texts_to_embed:
                embeddings = await self._embedding_provider.embed_batch(
                    [t[1] for t in texts_to_embed]
                )
                for (i, _), embedding in zip(texts_to_embed, embeddings):
                    documents[i].embedding = embedding
            
            # Add to ChromaDB
            self._collection.add(
                ids=[doc.id for doc in documents],
                embeddings=[doc.embedding for doc in documents],
                documents=[doc.content for doc in documents],
                metadatas=[doc.metadata for doc in documents],
            )
            
            logger.debug(f"Added {len(documents)} documents to vector store")
            return [doc.id for doc in documents]
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise VectorStoreError(f"Failed to add documents: {e}") from e
    
    async def search(
        self,
        query: str,
        n_results: int = 5,
        filter: dict | None = None,
    ) -> list[SearchResult]:
        """
        Search for similar documents.
        
        Parameters
        ----------
        query : str
            Search query (will be embedded).
        n_results : int, default=5
            Maximum results to return.
        filter : dict | None, optional
            Metadata filter (ChromaDB where clause).
        
        Returns
        -------
        list[SearchResult]
            Matching documents with scores.
        
        Raises
        ------
        VectorStoreError
            If search fails.
        """
        try:
            # Embed query
            query_embedding = await self._embedding_provider.embed(query)
            
            # Query ChromaDB
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter,
                include=["documents", "metadatas", "distances"],
            )
            
            # Convert to SearchResult
            search_results = []
            for i in range(len(results["ids"][0])):
                doc = VectorDocument(
                    id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                )
                search_results.append(SearchResult(
                    document=doc,
                    score=results["distances"][0][i],
                ))
            
            logger.debug(f"Search returned {len(search_results)} results for query: {query[:50]}...")
            return search_results
        except Exception as e:
            logger.error(f"Vector store search failed: {e}")
            raise VectorStoreError(f"Search failed: {e}") from e
    
    async def get(
        self,
        ids: list[str],
    ) -> list[VectorDocument]:
        """
        Retrieve documents by ID.
        
        Parameters
        ----------
        ids : list[str]
            Document IDs to retrieve.
        
        Returns
        -------
        list[VectorDocument]
            Retrieved documents.
        
        Raises
        ------
        VectorStoreError
            If retrieval fails.
        """
        try:
            results = self._collection.get(
                ids=ids,
                include=["documents", "metadatas"],
            )
            
            documents = []
            for i in range(len(results["ids"])):
                doc = VectorDocument(
                    id=results["ids"][i],
                    content=results["documents"][i],
                    metadata=results["metadatas"][i],
                )
                documents.append(doc)
            
            logger.debug(f"Retrieved {len(documents)} documents by ID")
            return documents
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {e}")
            raise VectorStoreError(f"Failed to retrieve documents: {e}") from e
    
    async def delete(
        self,
        ids: list[str],
    ) -> None:
        """
        Delete documents by ID.
        
        Parameters
        ----------
        ids : list[str]
            Document IDs to delete.
        
        Raises
        ------
        VectorStoreError
            If deletion fails.
        """
        try:
            self._collection.delete(ids=ids)
            logger.debug(f"Deleted {len(ids)} documents from vector store")
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            raise VectorStoreError(f"Failed to delete documents: {e}") from e
    
    async def count(self) -> int:
        """
        Return total document count.
        
        Returns
        -------
        int
            Number of documents in store.
        
        Raises
        ------
        VectorStoreError
            If count operation fails.
        """
        try:
            return self._collection.count()
        except Exception as e:
            logger.error(f"Failed to count documents: {e}")
            raise VectorStoreError(f"Failed to count documents: {e}") from e

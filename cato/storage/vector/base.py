"""Vector store protocol and data types."""

from typing import Protocol

from pydantic import BaseModel, ConfigDict


class VectorDocument(BaseModel):
    """
    Document stored in vector store.
    
    Uses Pydantic for validation as data crosses ChromaDB boundary.
    
    Parameters
    ----------
    id : str
        Unique document identifier.
    content : str
        Document text content.
    metadata : dict
        Additional metadata for filtering and retrieval.
    embedding : list[float] | None, optional
        Embedding vector. May not always be returned.
    """
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    content: str
    metadata: dict
    embedding: list[float] | None = None


class SearchResult(BaseModel):
    """
    Result from similarity search.
    
    Parameters
    ----------
    document : VectorDocument
        The matching document.
    score : float
        Distance/similarity score (lower is more similar for distance metrics).
    """
    
    document: VectorDocument
    score: float


class VectorStore(Protocol):
    """
    Protocol for vector store implementations.
    
    All operations are async to support potential remote backends.
    """
    
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
        """
        ...
    
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
        """
        ...
    
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
        """
        ...
    
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
        """
        ...
    
    async def count(self) -> int:
        """
        Return total document count.
        
        Returns
        -------
        int
            Number of documents in store.
        """
        ...

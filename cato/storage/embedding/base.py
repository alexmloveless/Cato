"""Embedding provider protocol."""

from typing import Protocol


class EmbeddingProvider(Protocol):
    """
    Protocol for embedding providers.
    
    Implementations generate vector embeddings for text.
    """
    
    async def embed(self, text: str) -> list[float]:
        """
        Generate embedding for single text.
        
        Parameters
        ----------
        text : str
            Text to embed.
        
        Returns
        -------
        list[float]
            Embedding vector.
        """
        ...
    
    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Parameters
        ----------
        texts : list[str]
            Texts to embed.
        batch_size : int, default=100
            Maximum texts per API call.
        
        Returns
        -------
        list[list[float]]
            Embedding vectors in same order as input texts.
        """
        ...

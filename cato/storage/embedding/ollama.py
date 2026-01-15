"""Ollama local embedding provider implementation."""

import logging

import httpx

from cato.core.exceptions import EmbeddingError

logger = logging.getLogger(__name__)


class OllamaEmbeddingProvider:
    """
    Ollama local embedding provider.
    
    Uses Ollama's local API for generating embeddings.
    
    Parameters
    ----------
    model : str
        Embedding model name (e.g., "nomic-embed-text").
    base_url : str, default="http://localhost:11434"
        Base URL for Ollama API.
    """
    
    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
    ) -> None:
        self._base_url = base_url
        self._model = model
        logger.info(f"Ollama embedding provider initialized with model={model}, base_url={base_url}")
    
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
        
        Raises
        ------
        EmbeddingError
            If embedding generation fails.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._base_url}/api/embeddings",
                    json={"model": self._model, "prompt": text},
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()["embedding"]
        except Exception as e:
            logger.error(f"Ollama embedding failed: {e}")
            raise EmbeddingError(f"Failed to generate embedding: {e}") from e
    
    async def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Ollama processes each text individually, so batch_size is for consistency
        with the protocol but doesn't affect API behavior.
        
        Parameters
        ----------
        texts : list[str]
            Texts to embed.
        batch_size : int, default=100
            Unused for Ollama (kept for protocol consistency).
        
        Returns
        -------
        list[list[float]]
            Embedding vectors in same order as input texts.
        
        Raises
        ------
        EmbeddingError
            If embedding generation fails.
        """
        embeddings = []
        
        try:
            async with httpx.AsyncClient() as client:
                for text in texts:
                    response = await client.post(
                        f"{self._base_url}/api/embeddings",
                        json={"model": self._model, "prompt": text},
                        timeout=30,
                    )
                    response.raise_for_status()
                    embeddings.append(response.json()["embedding"])
            
            return embeddings
        except Exception as e:
            logger.error(f"Ollama batch embedding failed: {e}")
            raise EmbeddingError(f"Failed to generate batch embeddings: {e}") from e

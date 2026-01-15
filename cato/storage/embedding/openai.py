"""OpenAI embedding provider implementation."""

import logging

from openai import AsyncOpenAI

from cato.core.exceptions import EmbeddingError

logger = logging.getLogger(__name__)


class OpenAIEmbeddingProvider:
    """
    OpenAI API embedding provider.
    
    Uses OpenAI's embedding models for generating vector embeddings.
    
    Parameters
    ----------
    api_key : str
        OpenAI API key.
    model : str, default="text-embedding-3-small"
        Embedding model to use.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ) -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        logger.info(f"OpenAI embedding provider initialized with model={model}")
    
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
            response = await self._client.embeddings.create(
                model=self._model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding failed: {e}")
            raise EmbeddingError(f"Failed to generate embedding: {e}") from e
    
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
        
        Raises
        ------
        EmbeddingError
            If embedding generation fails.
        """
        embeddings = []
        
        try:
            # Process in batches to respect API limits
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = await self._client.embeddings.create(
                    model=self._model,
                    input=batch,
                )
                embeddings.extend([d.embedding for d in response.data])
            
            return embeddings
        except Exception as e:
            logger.error(f"OpenAI batch embedding failed: {e}")
            raise EmbeddingError(f"Failed to generate batch embeddings: {e}") from e

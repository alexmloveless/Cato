"""Ollama local model provider implementation."""

import logging
from collections.abc import AsyncIterator

import httpx

from cato.core.config import OllamaConfig
from cato.core.exceptions import LLMConnectionError, LLMResponseError
from cato.core.types import CompletionResult, Message

logger = logging.getLogger(__name__)


class OllamaProvider:
    """
    Ollama local model provider implementation.
    
    Uses httpx to communicate with local Ollama server.
    
    Parameters
    ----------
    config : OllamaConfig
        Ollama-specific configuration.
    model : str
        Model identifier (e.g., 'llama2').
    temperature : float
        Default temperature.
    max_tokens : int
        Default max tokens.
    timeout : int
        Request timeout in seconds.
    """
    
    def __init__(
        self,
        config: OllamaConfig,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
    ) -> None:
        self._config = config
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._base_url = config.base_url
        self._timeout = timeout
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "ollama"
    
    @property
    def model(self) -> str:
        """Current model."""
        return self._model
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate completion using Ollama API.
        
        Parameters
        ----------
        messages : list[Message]
            Conversation history.
        temperature : float | None, optional
            Override temperature.
        max_tokens : int | None, optional
            Override max tokens.
        
        Returns
        -------
        CompletionResult
            Model response.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._base_url}/api/chat",
                    json={
                        "model": self._model,
                        "messages": [self._to_ollama_message(m) for m in messages],
                        "options": {
                            "temperature": temperature if temperature is not None else self._temperature,
                            "num_predict": max_tokens if max_tokens is not None else self._max_tokens,
                        },
                        "stream": False,
                    },
                    timeout=self._timeout,
                )
                response.raise_for_status()
                data = response.json()
                
                return CompletionResult(
                    content=data["message"]["content"],
                    model=self._model,
                )
                
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Ollama at {self._base_url}: {e}")
            raise LLMConnectionError(f"Cannot connect to Ollama at {self._base_url}: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e}")
            raise LLMResponseError(f"Ollama HTTP error: {e}")
        except Exception as e:
            logger.error(f"Unexpected Ollama error: {e}")
            raise LLMResponseError(f"Unexpected Ollama error: {e}")
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens from Ollama.
        
        Parameters
        ----------
        messages : list[Message]
            Conversation history.
        temperature : float | None, optional
            Override temperature.
        max_tokens : int | None, optional
            Override max tokens.
        
        Yields
        ------
        str
            Token chunks as they arrive.
        """
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{self._base_url}/api/chat",
                    json={
                        "model": self._model,
                        "messages": [self._to_ollama_message(m) for m in messages],
                        "options": {
                            "temperature": temperature if temperature is not None else self._temperature,
                            "num_predict": max_tokens if max_tokens is not None else self._max_tokens,
                        },
                        "stream": True,
                    },
                    timeout=self._timeout,
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
                                
        except httpx.ConnectError as e:
            raise LLMConnectionError(f"Cannot connect to Ollama: {e}")
        except Exception as e:
            raise LLMResponseError(f"Ollama streaming error: {e}")
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Parameters
        ----------
        text : str
            Text to count.
        
        Returns
        -------
        int
            Approximate token count.
        """
        return len(text) // 4
    
    async def close(self) -> None:
        """Close and cleanup resources (no-op for Ollama)."""
        logger.debug("Ollama provider closed")

    def _to_ollama_message(self, msg: Message) -> dict[str, str]:
        """Convert Message to Ollama format."""
        return {"role": msg.role, "content": msg.content}

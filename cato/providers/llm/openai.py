"""OpenAI API provider implementation."""

import logging
from collections.abc import AsyncIterator

import openai
from openai import AsyncOpenAI

from cato.core.config import OpenAIConfig
from cato.core.exceptions import (
    LLMAuthenticationError,
    LLMConnectionError,
    LLMContextLengthError,
    LLMRateLimitError,
    LLMResponseError,
)
from cato.core.types import CompletionResult, Message, TokenUsage

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """
    OpenAI API provider implementation.
    
    Supports GPT models via OpenAI's async client.
    
    Parameters
    ----------
    config : OpenAIConfig
        OpenAI-specific configuration.
    model : str
        Model identifier (e.g., 'gpt-4o-mini').
    temperature : float
        Default temperature.
    max_tokens : int
        Default max tokens.
    timeout : int
        Request timeout in seconds.
    """
    
    def __init__(
        self,
        config: OpenAIConfig,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
    ) -> None:
        self._config = config
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._client = AsyncOpenAI(api_key=config.api_key, timeout=timeout)
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "openai"
    
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
        Generate completion using OpenAI API.
        
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
            Model response with usage stats.
        
        Raises
        ------
        LLMAuthenticationError
            Invalid API key.
        LLMRateLimitError
            Rate limit exceeded.
        LLMConnectionError
            Connection failed.
        LLMContextLengthError
            Input too long.
        LLMResponseError
            Unexpected response format.
        """
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[self._to_openai_message(m) for m in messages],
                temperature=temperature if temperature is not None else self._temperature,
                max_tokens=max_tokens if max_tokens is not None else self._max_tokens,
            )
            return self._to_result(response)
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication failed: {e}")
            raise LLMAuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            retry_after = self._parse_retry_after(e)
            logger.warning(f"OpenAI rate limit hit, retry after: {retry_after}s")
            raise LLMRateLimitError(f"Rate limit exceeded: {e}", retry_after=retry_after)
        except openai.APIConnectionError as e:
            logger.error(f"OpenAI connection error: {e}")
            raise LLMConnectionError(f"Failed to connect to OpenAI: {e}")
        except openai.BadRequestError as e:
            # Often indicates context length exceeded
            if "context_length_exceeded" in str(e).lower():
                logger.error(f"Context length exceeded: {e}")
                raise LLMContextLengthError(f"Context length exceeded: {e}")
            logger.error(f"OpenAI bad request: {e}")
            raise LLMResponseError(f"Bad request: {e}")
        except Exception as e:
            logger.error(f"Unexpected OpenAI error: {e}")
            raise LLMResponseError(f"Unexpected error: {e}")
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens from OpenAI.
        
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
            stream = await self._client.chat.completions.create(
                model=self._model,
                messages=[self._to_openai_message(m) for m in messages],
                temperature=temperature if temperature is not None else self._temperature,
                max_tokens=max_tokens if max_tokens is not None else self._max_tokens,
                stream=True,
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except openai.AuthenticationError as e:
            raise LLMAuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            raise LLMRateLimitError(f"Rate limit exceeded: {e}")
        except openai.APIConnectionError as e:
            raise LLMConnectionError(f"Failed to connect to OpenAI: {e}")
    
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
            Approximate token count (rough estimate: 1 token ≈ 4 chars).
        """
        # Simple approximation - for accurate counting, would use tiktoken
        return len(text) // 4
    
    def _to_openai_message(self, msg: Message) -> dict[str, str]:
        """Convert Message to OpenAI format."""
        return {"role": msg.role, "content": msg.content}
    
    def _to_result(self, response: openai.types.chat.ChatCompletion) -> CompletionResult:
        """Convert OpenAI response to CompletionResult."""
        choice = response.choices[0]
        
        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )
        
        return CompletionResult(
            content=choice.message.content or "",
            model=response.model,
            usage=usage,
            finish_reason=choice.finish_reason,
        )
    
    async def close(self) -> None:
        """Close the OpenAI client and cleanup resources."""
        try:
            await self._client.close()
            logger.debug("OpenAI client closed")
        except Exception as e:
            logger.warning(f"Error closing OpenAI client: {e}")

    def _parse_retry_after(self, error: openai.RateLimitError) -> int | None:
        """Extract retry-after value from rate limit error."""
        # OpenAI typically includes retry-after in headers
        # For now, return None - could parse from error message
        return None

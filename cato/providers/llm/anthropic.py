"""Anthropic Claude API provider implementation."""

import logging
from collections.abc import AsyncIterator

import anthropic
from anthropic import AsyncAnthropic

from cato.core.config import AnthropicConfig
from cato.core.exceptions import (
    LLMAuthenticationError,
    LLMConnectionError,
    LLMRateLimitError,
    LLMResponseError,
)
from cato.core.types import CompletionResult, Message, TokenUsage

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """
    Anthropic Claude API provider implementation.
    
    Parameters
    ----------
    config : AnthropicConfig
        Anthropic-specific configuration.
    model : str
        Model identifier (e.g., 'claude-3-5-sonnet-20241022').
    temperature : float
        Default temperature.
    max_tokens : int
        Default max tokens.
    timeout : int
        Request timeout in seconds.
    """
    
    def __init__(
        self,
        config: AnthropicConfig,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
    ) -> None:
        self._config = config
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._client = AsyncAnthropic(api_key=config.api_key, timeout=timeout)
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "anthropic"
    
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
        Generate completion using Anthropic API.
        
        Anthropic handles system messages separately from chat messages.
        
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
        """
        # Extract system message (Anthropic handles it separately)
        system_msg = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = await self._client.messages.create(
                model=self._model,
                system=system_msg,
                messages=chat_messages,
                temperature=temperature if temperature is not None else self._temperature,
                max_tokens=max_tokens if max_tokens is not None else self._max_tokens,
            )
            return self._to_result(response)
            
        except anthropic.AuthenticationError as e:
            logger.error(f"Anthropic authentication failed: {e}")
            raise LLMAuthenticationError(f"Anthropic authentication failed: {e}")
        except anthropic.RateLimitError as e:
            logger.warning(f"Anthropic rate limit hit: {e}")
            raise LLMRateLimitError(f"Rate limit exceeded: {e}")
        except anthropic.APIConnectionError as e:
            logger.error(f"Anthropic connection error: {e}")
            raise LLMConnectionError(f"Failed to connect to Anthropic: {e}")
        except Exception as e:
            logger.error(f"Unexpected Anthropic error: {e}")
            raise LLMResponseError(f"Unexpected error: {e}")
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens from Anthropic.
        
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
        system_msg = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})
        
        try:
            async with self._client.messages.stream(
                model=self._model,
                system=system_msg,
                messages=chat_messages,
                temperature=temperature if temperature is not None else self._temperature,
                max_tokens=max_tokens if max_tokens is not None else self._max_tokens,
            ) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except anthropic.AuthenticationError as e:
            raise LLMAuthenticationError(f"Anthropic authentication failed: {e}")
        except anthropic.RateLimitError as e:
            raise LLMRateLimitError(f"Rate limit exceeded: {e}")
        except anthropic.APIConnectionError as e:
            raise LLMConnectionError(f"Failed to connect to Anthropic: {e}")
    
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
        return len(text) // 4
    
    async def close(self) -> None:
        """Close the Anthropic client and cleanup resources."""
        try:
            await self._client.close()
            logger.debug("Anthropic client closed")
        except Exception as e:
            logger.warning(f"Error closing Anthropic client: {e}")

    def _to_result(self, response: anthropic.types.Message) -> CompletionResult:
        """Convert Anthropic response to CompletionResult."""
        content = "".join(block.text for block in response.content if hasattr(block, "text"))

        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            )

        return CompletionResult(
            content=content,
            model=response.model,
            usage=usage,
            finish_reason=response.stop_reason,
        )

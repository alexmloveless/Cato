"""LLM provider protocol definition."""

from collections.abc import AsyncIterator
from typing import Protocol

from cato.core.types import CompletionResult, Message


class LLMProvider(Protocol):
    """
    Protocol for LLM provider implementations.
    
    Any class implementing these methods can be used as a provider.
    Providers are responsible for translating between Cato's normalized
    message format and provider-specific APIs.
    """
    
    @property
    def name(self) -> str:
        """
        Provider identifier.
        
        Returns
        -------
        str
            Provider name (e.g., 'openai', 'anthropic', 'google', 'ollama').
        """
        ...
    
    @property
    def model(self) -> str:
        """
        Currently configured model identifier.
        
        Returns
        -------
        str
            Model name (e.g., 'gpt-4o-mini', 'claude-3-5-sonnet-20241022').
        """
        ...
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate a completion for the given messages.
        
        Parameters
        ----------
        messages : list[Message]
            Conversation history in normalized format. System messages,
            if present, should be handled appropriately by the provider.
        temperature : float | None, optional
            Override configured temperature (0.0-2.0).
        max_tokens : int | None, optional
            Override configured max tokens.
        
        Returns
        -------
        CompletionResult
            The model's response with metadata.
        
        Raises
        ------
        LLMConnectionError
            Cannot reach the provider.
        LLMAuthenticationError
            Invalid API key.
        LLMRateLimitError
            Rate limit exceeded.
        LLMContextLengthError
            Input exceeds context window.
        LLMResponseError
            Invalid or unexpected response.
        """
        ...
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens as they arrive.
        
        Parameters
        ----------
        messages : list[Message]
            Conversation history in normalized format.
        temperature : float | None, optional
            Override configured temperature.
        max_tokens : int | None, optional
            Override configured max tokens.
        
        Yields
        ------
        str
            Individual tokens or token chunks as they're generated.
        
        Raises
        ------
        LLMConnectionError
            Cannot reach the provider.
        LLMAuthenticationError
            Invalid API key.
        LLMRateLimitError
            Rate limit exceeded.
        LLMContextLengthError
            Input exceeds context window.
        """
        ...
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text for this provider's tokenizer.
        
        Parameters
        ----------
        text : str
            Text to tokenize.
        
        Returns
        -------
        int
            Approximate token count.
        
        Notes
        -----
        Implementation may use provider-specific tokenizers or approximations.
        """
        ...

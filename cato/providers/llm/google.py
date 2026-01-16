"""Google Gemini API provider implementation."""

import logging
import warnings
from collections.abc import AsyncIterator

# Suppress deprecation warning for google.generativeai
# This package is deprecated but still functional. Migration to google.genai
# should be done in a future update when the new package is stable.
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
warnings.resetwarnings()  # Reset filter after import

from cato.core.config import GoogleConfig
from cato.core.exceptions import LLMConnectionError, LLMResponseError
from cato.core.types import CompletionResult, Message

logger = logging.getLogger(__name__)


class GoogleProvider:
    """
    Google Gemini API provider implementation.
    
    Parameters
    ----------
    config : GoogleConfig
        Google-specific configuration.
    model : str
        Model identifier (e.g., 'gemini-pro').
    temperature : float
        Default temperature.
    max_tokens : int
        Default max tokens.
    """
    
    def __init__(
        self,
        config: GoogleConfig,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
    ) -> None:
        self._config = config
        self._model_name = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        genai.configure(api_key=config.api_key)
        self._model = genai.GenerativeModel(model)
    
    @property
    def name(self) -> str:
        """Provider name."""
        return "google"
    
    @property
    def model(self) -> str:
        """Current model."""
        return self._model_name
    
    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate completion using Google Gemini API.
        
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
            # Convert to Gemini format
            history = self._build_history(messages[:-1])
            chat = self._model.start_chat(history=history)
            
            generation_config = genai.GenerationConfig(
                temperature=temperature if temperature is not None else self._temperature,
                max_output_tokens=max_tokens if max_tokens is not None else self._max_tokens,
            )
            
            response = await chat.send_message_async(
                messages[-1].content,
                generation_config=generation_config,
            )
            
            return CompletionResult(
                content=response.text,
                model=self._model_name,
            )
            
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise LLMResponseError(f"Google API error: {e}")
    
    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream completion tokens from Google.
        
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
            history = self._build_history(messages[:-1])
            chat = self._model.start_chat(history=history)
            
            generation_config = genai.GenerationConfig(
                temperature=temperature if temperature is not None else self._temperature,
                max_output_tokens=max_tokens if max_tokens is not None else self._max_tokens,
            )
            
            response = await chat.send_message_async(
                messages[-1].content,
                generation_config=generation_config,
                stream=True,
            )
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            raise LLMConnectionError(f"Google streaming error: {e}")
    
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
    
    def _build_history(self, messages: list[Message]) -> list[dict[str, str]]:
        """
        Build Gemini chat history from messages.
        
        Parameters
        ----------
        messages : list[Message]
            Messages to convert (excluding system and last message).
        
        Returns
        -------
        list[dict[str, str]]
            Gemini-formatted history.
        """
        history = []
        for msg in messages:
            if msg.role != "system":
                # Gemini uses 'user' and 'model' roles
                role = "model" if msg.role == "assistant" else "user"
                history.append({"role": role, "parts": [msg.content]})
        return history

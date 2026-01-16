"""Mock LLM provider for testing and dummy mode."""

import logging
from collections.abc import AsyncIterator

from cato.core.types import CompletionResult, Message

logger = logging.getLogger(__name__)


class MockLLMProvider:
    """
    Mock LLM provider that returns deterministic responses.

    Used when --dummy-mode flag is set. Does not make external API calls.

    Parameters
    ----------
    model : str, optional
        Model identifier to report (default: "mock-model").
    """

    def __init__(self, model: str = "mock-model") -> None:
        self._model = model
        logger.info("MockLLMProvider initialized")

    @property
    def name(self) -> str:
        """Provider identifier."""
        return "mock"

    @property
    def model(self) -> str:
        """Currently configured model identifier."""
        return self._model

    async def complete(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Generate a mock completion response.

        Parameters
        ----------
        messages : list[Message]
            Conversation history (inspected to generate contextual response).
        temperature : float | None, optional
            Ignored in mock mode.
        max_tokens : int | None, optional
            Ignored in mock mode.

        Returns
        -------
        CompletionResult
            Mock response with metadata.
        """
        # Get last user message for context
        user_messages = [m for m in messages if m.role == "user"]
        last_message = user_messages[-1].content if user_messages else ""

        # Generate deterministic response based on input
        response_content = self._generate_mock_response(last_message)

        logger.debug(f"Mock completion generated: {len(response_content)} chars")

        return CompletionResult(
            content=response_content,
            model=self._model,
            provider="mock",
            usage={
                "prompt_tokens": sum(len(m.content.split()) for m in messages),
                "completion_tokens": len(response_content.split()),
                "total_tokens": sum(len(m.content.split()) for m in messages) + len(response_content.split()),
            },
        )

    async def complete_stream(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream mock completion tokens.

        Parameters
        ----------
        messages : list[Message]
            Conversation history.
        temperature : float | None, optional
            Ignored in mock mode.
        max_tokens : int | None, optional
            Ignored in mock mode.

        Yields
        ------
        str
            Individual tokens from mock response.
        """
        # Generate full response
        result = await self.complete(messages, temperature=temperature, max_tokens=max_tokens)

        # Yield word by word to simulate streaming
        words = result.content.split()
        for i, word in enumerate(words):
            if i < len(words) - 1:
                yield word + " "
            else:
                yield word

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using simple word splitting.

        Parameters
        ----------
        text : str
            Text to tokenize.

        Returns
        -------
        int
            Approximate token count (word count).
        """
        return len(text.split())

    def _generate_mock_response(self, user_input: str) -> str:
        """
        Generate deterministic mock response based on user input.

        Parameters
        ----------
        user_input : str
            User's input message.

        Returns
        -------
        str
            Mock response content.
        """
        # Simple pattern matching for common queries
        lower_input = user_input.lower()

        if "hello" in lower_input or "hi" in lower_input:
            return "Hello! This is a mock response from Cato running in dummy mode. How can I help you today?"

        if "help" in lower_input:
            return "This is a mock response. In dummy mode, Cato uses a mock LLM provider that returns placeholder responses without making external API calls."

        if "?" in user_input:
            return f"This is a mock answer to your question. In dummy mode, responses are deterministic placeholders for testing purposes."

        # Default response
        return (
            f"Mock response to: '{user_input[:50]}...'\n\n"
            "This is a placeholder response generated in dummy mode. "
            "No external API calls are being made. "
            "Dummy mode is useful for testing Cato's interface and commands without consuming API credits."
        )

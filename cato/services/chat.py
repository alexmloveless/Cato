"""
Chat service for orchestrating LLM interactions.

This module provides the ChatService class which coordinates between conversation
management, LLM providers, and vector store retrieval to handle chat completions.
"""

import asyncio
from pathlib import Path
from typing import AsyncIterator

from cato.core.config import CatoConfig
from cato.core.exceptions import LLMConnectionError, LLMRateLimitError, LLMError
from cato.core.logging import get_logger
from cato.core.types import CompletionResult
from cato.providers.llm.base import LLMProvider
from cato.services.conversation import Conversation

logger = get_logger(__name__)


class ChatService:
    """
    Orchestrates chat interactions with LLM providers.

    This service manages conversation state, system prompts, token truncation,
    and coordinates with the LLM provider to generate responses.

    Parameters
    ----------
    provider : LLMProvider
        LLM provider instance for completions.
    config : CatoConfig
        Application configuration.
    system_prompt : str, optional
        System prompt to use. If not provided, loads from config or default.

    Attributes
    ----------
    provider : LLMProvider
        The configured LLM provider.
    config : CatoConfig
        Application configuration.
    conversation : Conversation
        Current conversation state.
    """

    def __init__(
        self,
        provider: LLMProvider,
        config: CatoConfig,
        system_prompt: str | None = None,
    ) -> None:
        """
        Initialize chat service.

        Parameters
        ----------
        provider : LLMProvider
            LLM provider for completions.
        config : CatoConfig
            Application configuration.
        system_prompt : str, optional
            Override system prompt (default: load from config/defaults).
        """
        self.provider = provider
        self.config = config
        self.conversation = Conversation(
            system_prompt=system_prompt or self._load_system_prompt()
        )
        logger.info(
            f"ChatService initialized with provider={provider.name}, model={provider.model}"
        )

    def _load_system_prompt(self) -> str:
        """
        Load system prompt from configuration or package defaults.

        Returns
        -------
        str
            Complete system prompt.

        Notes
        -----
        Handles three scenarios:
        1. base_prompt_file with override_base_prompt=True: use only custom prompt
        2. base_prompt_file with override_base_prompt=False: default + custom
        3. No base_prompt_file: use default + system_prompt_files
        """
        # Default package prompt
        default_prompt_path = Path(__file__).parent.parent / "resources" / "system_prompt.txt"
        
        # Start with default or custom base
        if self.config.llm.base_prompt_file and self.config.llm.override_base_prompt:
            # Complete override: use only the custom base
            base_prompt = self._read_prompt_file(Path(self.config.llm.base_prompt_file))
            logger.info(f"Using override base prompt from {self.config.llm.base_prompt_file}")
        else:
            # Start with default
            if default_prompt_path.exists():
                base_prompt = default_prompt_path.read_text().strip()
            else:
                # Fallback if package file missing
                base_prompt = "You are Cato, a helpful AI assistant."
                logger.warning("Default system prompt file not found, using fallback")
            
            # Append custom base if provided (non-override mode)
            if self.config.llm.base_prompt_file:
                custom_base = self._read_prompt_file(Path(self.config.llm.base_prompt_file))
                base_prompt = f"{base_prompt}\n\n{custom_base}"
                logger.info(f"Appended base prompt from {self.config.llm.base_prompt_file}")
        
        # Append additional system prompt files
        for prompt_file in self.config.llm.system_prompt_files:
            additional = self._read_prompt_file(Path(prompt_file))
            base_prompt = f"{base_prompt}\n\n{additional}"
            logger.info(f"Appended system prompt from {prompt_file}")
        
        return base_prompt

    def _read_prompt_file(self, path: Path) -> str:
        """
        Read and validate a prompt file.

        Parameters
        ----------
        path : Path
            Path to prompt file.

        Returns
        -------
        str
            Prompt content.

        Raises
        ------
        FileNotFoundError
            If prompt file doesn't exist.
        """
        expanded_path = path.expanduser().resolve()
        if not expanded_path.exists():
            raise FileNotFoundError(f"System prompt file not found: {expanded_path}")
        return expanded_path.read_text().strip()

    async def send_message(
        self,
        user_message: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> CompletionResult:
        """
        Send a user message and get LLM response.

        This method adds the user message to conversation history, optionally
        truncates to fit token limits, sends to the LLM, and stores the response.

        Parameters
        ----------
        user_message : str
            User's message content.
        temperature : float, optional
            Override configured temperature.
        max_tokens : int, optional
            Override configured max tokens.

        Returns
        -------
        CompletionResult
            LLM response with metadata.

        Raises
        ------
        LLMError
            If completion fails after retries.
        """
        # Add user message to history
        self.conversation.add_user_message(user_message)
        logger.debug(f"Added user message (length={len(user_message)})")

        # Truncate conversation to fit within context window if needed
        # Reserve ~20% of max_tokens for the response
        context_limit = int((max_tokens or self.config.llm.max_tokens) * 0.8)
        self.conversation.truncate_to_tokens(context_limit, self.provider.count_tokens)
        
        # Get messages for LLM
        messages = self.conversation.to_messages()
        logger.debug(f"Sending {len(messages)} messages to LLM")

        # Get completion with retry logic
        result = await self._complete_with_retry(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Add assistant response to history
        self.conversation.add_assistant_message(result.content)
        logger.info(
            f"Completed message exchange (tokens: {result.usage.total_tokens if result.usage else 'unknown'})"
        )

        return result

    async def send_message_stream(
        self,
        user_message: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """
        Send a user message and stream LLM response tokens.

        Similar to send_message but yields tokens as they arrive rather than
        waiting for complete response.

        Parameters
        ----------
        user_message : str
            User's message content.
        temperature : float, optional
            Override configured temperature.
        max_tokens : int, optional
            Override configured max tokens.

        Yields
        ------
        str
            Individual tokens or token chunks from the LLM.

        Notes
        -----
        The complete response is stored in conversation history after streaming completes.
        """
        # Add user message to history
        self.conversation.add_user_message(user_message)
        logger.debug(f"Added user message for streaming (length={len(user_message)})")

        # Truncate conversation
        context_limit = int((max_tokens or self.config.llm.max_tokens) * 0.8)
        self.conversation.truncate_to_tokens(context_limit, self.provider.count_tokens)

        # Get messages for LLM
        messages = self.conversation.to_messages()
        logger.debug(f"Streaming {len(messages)} messages to LLM")

        # Collect full response while streaming
        full_response = []
        async for token in self.provider.complete_stream(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            full_response.append(token)
            yield token

        # Store complete response in history
        response_text = "".join(full_response)
        self.conversation.add_assistant_message(response_text)
        logger.info(f"Completed streaming exchange (response length={len(response_text)})")

    async def _complete_with_retry(
        self,
        messages: list,
        temperature: float | None = None,
        max_tokens: int | None = None,
        max_retries: int = 3,
    ) -> CompletionResult:
        """
        Execute LLM completion with automatic retry on transient failures.

        Parameters
        ----------
        messages : list
            Messages to send to LLM.
        temperature : float, optional
            Temperature override.
        max_tokens : int, optional
            Max tokens override.
        max_retries : int
            Maximum number of retry attempts (default: 3).

        Returns
        -------
        CompletionResult
            Successful completion result.

        Raises
        ------
        LLMError
            After all retries exhausted.
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return await self.provider.complete(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except LLMRateLimitError as e:
                last_error = e
                # Respect retry-after header if available
                wait_time = e.retry_after if e.retry_after else (2 ** attempt)
                logger.warning(
                    f"Rate limit hit (attempt {attempt + 1}/{max_retries}), "
                    f"waiting {wait_time}s"
                )
                await asyncio.sleep(wait_time)
            except LLMConnectionError as e:
                last_error = e
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(
                    f"Connection error (attempt {attempt + 1}/{max_retries}), "
                    f"waiting {wait_time}s: {e}"
                )
                await asyncio.sleep(wait_time)
        
        # All retries exhausted
        logger.error(f"Max retries ({max_retries}) exhausted")
        raise last_error or LLMError("Max retries exceeded")

    def clear_conversation(self) -> None:
        """
        Clear conversation history while preserving system prompt.

        This resets the conversation to its initial state.
        """
        self.conversation.clear()
        logger.info("Conversation history cleared")

    def get_message_count(self) -> int:
        """
        Get number of messages in conversation history.

        Returns
        -------
        int
            Message count (excludes system prompt).
        """
        return self.conversation.message_count()

    def update_system_prompt(self, new_prompt: str) -> None:
        """
        Update the system prompt for future interactions.

        Parameters
        ----------
        new_prompt : str
            New system prompt text.

        Notes
        -----
        This does not affect existing conversation history, only future LLM calls.
        """
        self.conversation.system_prompt = new_prompt
        logger.info("System prompt updated")

"""
Conversation management for chat sessions.

This module provides the Conversation class for managing message history,
system prompts, and token-aware truncation.
"""

from dataclasses import dataclass, field
from typing import Callable

from cato.core.types import Message


@dataclass
class Conversation:
    """
    Manages conversation state and history.

    This class tracks the system prompt and message history for a chat session,
    providing methods to add messages and truncate history to fit within token limits.

    Parameters
    ----------
    system_prompt : str
        System prompt to prepend to all LLM requests.
    messages : list[Message], optional
        Initial message history (default: empty list).

    Attributes
    ----------
    system_prompt : str
        Current system prompt.
    messages : list[Message]
        Conversation message history (user and assistant messages only).
    """

    system_prompt: str
    messages: list[Message] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        """
        Add a user message to conversation history.

        Parameters
        ----------
        content : str
            User message content.
        """
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant response to conversation history.

        Parameters
        ----------
        content : str
            Assistant message content.
        """
        self.messages.append(Message(role="assistant", content=content))

    def to_messages(self) -> list[Message]:
        """
        Get full message list for LLM request.

        Returns the system prompt as the first message, followed by all
        conversation messages.

        Returns
        -------
        list[Message]
            Complete message list (system + history).
        """
        return [Message(role="system", content=self.system_prompt)] + self.messages

    def truncate_to_tokens(self, max_tokens: int, counter: Callable[[str], int]) -> None:
        """
        Truncate conversation history to fit within token limit.

        Removes oldest messages (after system prompt) until the total token count
        is within the specified limit. Always preserves the system prompt and the
        most recent exchange (last 2 messages).

        Parameters
        ----------
        max_tokens : int
            Maximum allowed token count.
        counter : Callable[[str], int]
            Function to count tokens in text (e.g., provider.count_tokens).

        Notes
        -----
        - System prompt is always kept
        - Last 2 messages are preserved when possible
        - Removes messages from oldest to newest
        """
        # Keep removing oldest messages until we're under the limit
        # Always keep at least the last 2 messages (most recent exchange)
        while self._count_tokens(counter) > max_tokens and len(self.messages) > 2:
            self.messages.pop(0)

    def _count_tokens(self, counter: Callable[[str], int]) -> int:
        """
        Count total tokens in conversation (system + all messages).

        Parameters
        ----------
        counter : Callable[[str], int]
            Token counting function.

        Returns
        -------
        int
            Total token count.
        """
        total = counter(self.system_prompt)
        for msg in self.messages:
            total += counter(msg.content)
        return total

    def clear(self) -> None:
        """
        Clear all messages from conversation history.

        The system prompt is preserved.
        """
        self.messages.clear()

    def message_count(self) -> int:
        """
        Get the number of messages in history (excluding system prompt).

        Returns
        -------
        int
            Message count.
        """
        return len(self.messages)

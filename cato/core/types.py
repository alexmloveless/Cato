"""Shared data types used across Cato modules."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Normalised message format for chat conversations.
    
    Parameters
    ----------
    role : Literal["system", "user", "assistant"]
        The role of the message sender.
    content : str
        The message content.
    """
    
    role: Literal["system", "user", "assistant"]
    content: str


class TokenUsage(BaseModel):
    """
    Token usage statistics from LLM completion.
    
    Parameters
    ----------
    prompt_tokens : int
        Number of tokens in the prompt.
    completion_tokens : int
        Number of tokens in the completion.
    total_tokens : int
        Total tokens used (prompt + completion).
    """
    
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResult(BaseModel):
    """
    Result from LLM completion request.
    
    Parameters
    ----------
    content : str
        The generated text content.
    model : str
        The model that generated the response.
    usage : TokenUsage | None, optional
        Token usage statistics if available.
    finish_reason : str | None, optional
        Reason the generation stopped (e.g., "stop", "length").
    """
    
    content: str
    model: str
    usage: TokenUsage | None = None
    finish_reason: str | None = None


class ConversationExchange(BaseModel):
    """
    A single user-assistant exchange for vector store storage.

    Parameters
    ----------
    user_message : str
        The user's input message.
    assistant_message : str
        The assistant's response.
    timestamp : str
        ISO format timestamp of the exchange.
    session_id : str | None, optional
        Session identifier for grouping related exchanges.
    thread_id : str | None, optional
        Thread identifier for conversation continuation.
    """

    user_message: str
    assistant_message: str
    timestamp: str
    session_id: str | None = None
    thread_id: str | None = None


class List(BaseModel):
    """
    Named list metadata.

    Attributes
    ----------
    name : str
        Unique list name.
    description : str | None
        Optional description.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    metadata : dict
        Extensible metadata.
    """
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    metadata: dict = Field(default_factory=dict)


class ListItem(BaseModel):
    """
    Item in a list.

    Attributes
    ----------
    id : int | None
        Globally unique auto-incrementing ID.
    list_name : str
        Name of parent list.
    description : str
        Item content.
    status : Literal
        Item status (pending, active, in_progress, done).
    priority : Literal
        Priority level (urgent, high, medium, low).
    category : str | None
        Optional category.
    tags : list[str]
        List of tags.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    metadata : dict
        Extensible metadata.
    """
    id: int | None = None  # None for new items
    list_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1, max_length=500)
    status: Literal["pending", "active", "in_progress", "done"] = "pending"
    priority: Literal["urgent", "high", "medium", "low"] = "medium"
    category: str | None = Field(None, max_length=50)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)

    @property
    def display_id(self) -> str:
        """Format ID as zero-padded 3-digit string."""
        return f"{self.id:03d}" if self.id else "???"

    @property
    def priority_order(self) -> int:
        """Return integer for priority sorting (1=urgent, 4=low)."""
        priority_map = {"urgent": 1, "high": 2, "medium": 3, "low": 4}
        return priority_map[self.priority]

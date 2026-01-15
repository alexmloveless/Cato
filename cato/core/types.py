"""Shared data types used across Cato modules."""

from typing import Literal

from pydantic import BaseModel


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

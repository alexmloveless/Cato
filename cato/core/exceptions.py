"""Exception hierarchy for Cato application."""

from typing import Any


class CatoError(Exception):
    """
    Base exception for all Cato errors.
    
    All custom exceptions inherit from this to enable catching
    any Cato-specific error with a single except clause when needed.
    
    Parameters
    ----------
    message : str
        Human-readable error description.
    context : dict[str, Any] | None, optional
        Optional dict of contextual data for debugging.
    """
    
    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}
    
    def __str__(self) -> str:
        if self.context:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{self.message} ({ctx})"
        return self.message


# Configuration exceptions
class ConfigurationError(CatoError):
    """Configuration loading or validation error."""


class ConfigFileNotFoundError(ConfigurationError):
    """Required configuration file missing."""


class ConfigValidationError(ConfigurationError):
    """Configuration value failed validation."""


# LLM Provider exceptions
class LLMError(CatoError):
    """LLM provider or API error."""


class LLMConnectionError(LLMError):
    """Cannot connect to LLM provider."""


class LLMAuthenticationError(LLMError):
    """API key invalid or missing."""


class LLMRateLimitError(LLMError):
    """
    Rate limit exceeded.
    
    Parameters
    ----------
    message : str
        Human-readable error description.
    retry_after : int | None, optional
        Seconds to wait before retrying.
    context : dict[str, Any] | None, optional
        Optional dict of contextual data for debugging.
    """
    
    def __init__(
        self,
        message: str,
        retry_after: int | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, context)
        self.retry_after = retry_after


class LLMContextLengthError(LLMError):
    """Input exceeds model context window."""


class LLMResponseError(LLMError):
    """Invalid or unexpected response from LLM."""


# Vector Store exceptions
class VectorStoreError(CatoError):
    """Vector store operation error."""


class VectorStoreConnectionError(VectorStoreError):
    """Cannot connect to vector store."""


class EmbeddingError(VectorStoreError):
    """Error generating embeddings."""


# Storage (SQLite) exceptions
class StorageError(CatoError):
    """Database storage error."""


class StorageConnectionError(StorageError):
    """Cannot connect to database."""


class StorageQueryError(StorageError):
    """Database query failed."""


# Command exceptions
class CommandError(CatoError):
    """Command execution error."""


class CommandNotFoundError(CommandError):
    """Unknown command."""


class CommandArgumentError(CommandError):
    """Invalid command arguments."""


class CommandExecutionError(CommandError):
    """Command failed during execution."""


# Input/Output exceptions
class IOError(CatoError):
    """File or network I/O error."""


class FileAccessError(IOError):
    """Cannot read or write file."""


class NetworkError(IOError):
    """Network operation failed."""


# TTS Provider exceptions
class TTSError(CatoError):
    """TTS provider or API error."""


class TTSConnectionError(TTSError):
    """Cannot connect to TTS provider."""


class TTSAuthenticationError(TTSError):
    """API key invalid or missing."""


class TTSRateLimitError(TTSError):
    """
    Rate limit exceeded.

    Parameters
    ----------
    message : str
        Human-readable error description.
    retry_after : int | None, optional
        Seconds to wait before retrying.
    context : dict[str, Any] | None, optional
        Optional dict of contextual data for debugging.
    """

    def __init__(
        self,
        message: str,
        retry_after: int | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, context)
        self.retry_after = retry_after


class TTSInvalidInputError(TTSError):
    """Invalid voice, model, or text input."""


# Display exceptions
class DisplayError(CatoError):
    """Display/rendering error."""

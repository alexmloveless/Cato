"""Command base types and protocol."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from cato.core.config import CatoConfig


@dataclass
class CommandResult:
    """
    Result from command execution.
    
    Note: Uses dataclass as it's internal return data, not external.
    
    Parameters
    ----------
    success : bool
        Whether command succeeded.
    message : str
        Result message.
    data : dict[str, Any] | None, optional
        Optional result data.
    """
    
    success: bool
    message: str
    data: dict[str, Any] | None = None


@dataclass
class CommandContext:
    """
    Execution context providing access to application services.
    
    Injected at runtime—commands should not instantiate dependencies.
    Uses dataclass as it's a dependency container, not external data.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration.
    conversation : Conversation
        Current conversation state.
    llm : LLMProvider
        LLM provider instance.
    vector_store : VectorStore | None
        Vector store if enabled.
    storage : Storage
        Storage service.
    display : Display
        Display implementation.
    cwd : Path
        Current working directory.
    session_id : str
        Current session ID.
    thread_id : str | None
        Current thread ID if any.
    registry : CommandRegistry | None
        Command registry for command lookup.
    """
    
    config: "CatoConfig"
    conversation: Any  # Will be Conversation from services
    llm: Any  # Will be LLMProvider
    vector_store: Any | None  # Will be VectorStore
    storage: Any  # Will be Storage
    display: Any  # Will be Display
    cwd: Path = field(default_factory=lambda: Path.cwd())
    session_id: str = ""
    thread_id: str | None = None
    registry: Any | None = None  # Will be CommandRegistry


class Command(Protocol):
    """
    Protocol for command implementations.
    
    Commands are stateless—all state accessed via injected dependencies.
    """
    
    @property
    def name(self) -> str:
        """Primary command name (without slash)."""
        ...
    
    @property
    def aliases(self) -> list[str]:
        """Alternative names for the command."""
        ...
    
    @property
    def description(self) -> str:
        """Brief description for help text."""
        ...
    
    @property
    def usage(self) -> str:
        """Usage pattern string."""
        ...
    
    async def execute(
        self,
        args: list[str],
        context: CommandContext,
    ) -> CommandResult:
        """
        Execute the command.
        
        Parameters
        ----------
        args : list[str]
            Parsed arguments (command name excluded).
        context : CommandContext
            Execution context with dependencies.
        
        Returns
        -------
        CommandResult
            Result with success status and message.
        """
        ...

"""Display protocol and base types."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol


@dataclass
class DisplayMessage:
    """
    Display message data.
    
    Note: Uses dataclass as it's internal display data, not external.
    Named DisplayMessage to avoid confusion with LLM Message model.
    
    Parameters
    ----------
    role : Literal["user", "assistant", "system", "error", "info"]
        Message role for styling.
    content : str
        Message content.
    timestamp : datetime | None, optional
        Optional timestamp for display.
    """
    
    role: Literal["user", "assistant", "system", "error", "info"]
    content: str
    timestamp: datetime | None = None


class Display(Protocol):
    """
    Protocol for display implementations.
    
    Abstracts terminal output to enable pluggable frontends.
    """
    
    def show_message(self, message: DisplayMessage) -> None:
        """
        Display a message.
        
        Parameters
        ----------
        message : DisplayMessage
            Message to display with role-based styling.
        """
        ...
    
    def show_error(self, error: str, details: str | None = None) -> None:
        """
        Display an error message.
        
        Parameters
        ----------
        error : str
            Error message.
        details : str | None, optional
            Optional additional details.
        """
        ...
    
    def show_warning(self, warning: str) -> None:
        """
        Display a warning message.
        
        Parameters
        ----------
        warning : str
            Warning message.
        """
        ...
    
    def show_info(self, info: str) -> None:
        """
        Display an informational message.
        
        Parameters
        ----------
        info : str
            Info message.
        """
        ...
    
    def show_markdown(self, content: str) -> None:
        """
        Display markdown-formatted content.
        
        Parameters
        ----------
        content : str
            Markdown text.
        """
        ...
    
    def show_code(self, code: str, language: str | None = None) -> None:
        """
        Display syntax-highlighted code.
        
        Parameters
        ----------
        code : str
            Code to display.
        language : str | None, optional
            Language for syntax highlighting.
        """
        ...
    
    def show_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        title: str | None = None,
    ) -> None:
        """
        Display a table.
        
        Parameters
        ----------
        headers : list[str]
            Column headers.
        rows : list[list[str]]
            Table rows.
        title : str | None, optional
            Optional table title.
        """
        ...
    
    def show_spinner(self, message: str) -> "SpinnerContext":
        """
        Show a loading spinner.
        
        Parameters
        ----------
        message : str
            Message to show while loading.
        
        Returns
        -------
        SpinnerContext
            Context manager that stops spinner on exit.
        """
        ...
    
    def clear(self) -> None:
        """Clear the terminal screen."""
        ...
    
    def show_welcome(self) -> None:
        """Display welcome message."""
        ...


class SpinnerContext(Protocol):
    """Protocol for spinner context managers."""
    
    def __enter__(self) -> "SpinnerContext":
        """Start spinner."""
        ...
    
    def __exit__(self, *args: object) -> None:
        """Stop spinner."""
        ...
    
    def update(self, message: str) -> None:
        """
        Update spinner message.
        
        Parameters
        ----------
        message : str
            New message.
        """
        ...

"""Rich-based terminal display implementation."""

import logging
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.table import Table

from cato.core.config import DisplayConfig
from cato.display.base import DisplayMessage
from cato.display.themes import load_theme

logger = logging.getLogger(__name__)


class RichDisplay:
    """
    Rich-based terminal display implementation.
    
    Parameters
    ----------
    config : DisplayConfig
        Display configuration.
    """
    
    def __init__(self, config: DisplayConfig) -> None:
        self._config = config
        theme = load_theme(config.theme, config.style_overrides)
        self._console = Console(
            theme=theme,
            width=config.max_width,
            soft_wrap=config.soft_wrap,
            force_terminal=config.force_terminal,
        )
    
    def show_message(self, message: DisplayMessage) -> None:
        """Display a message with role-based styling."""
        prefix = self._get_prefix(message.role)
        style = message.role

        if self._config.timestamps and message.timestamp:
            timestamp = message.timestamp.strftime("%H:%M")
            prefix = f"[dim]{timestamp}[/dim] {prefix}"

        # Add spacing before message
        self._console.print()

        if message.role == "assistant" and self._config.markdown_enabled:
            self._console.print(prefix, style=style)
            self._console.print(
                Markdown(message.content, code_theme=self._config.code_theme),
                soft_wrap=self._config.soft_wrap,
            )
            # Add horizontal rule after assistant response
            self._console.print()
            self._console.print(Rule(style="dim"))
            return

        # Non-markdown / non-assistant: avoid composing a single long f-string so Rich can wrap cleanly.
        self._console.print(prefix, message.content, style=style, soft_wrap=self._config.soft_wrap)

        # Add spacing after user messages
        if message.role == "user":
            self._console.print()
    
    def _get_prefix(self, role: str) -> str:
        """Get display prefix for role."""
        prefixes = {
            "user": "You:",
            "assistant": "Cato:",
            "system": "System:",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
        }
        return prefixes.get(role, "")
    
    def show_error(self, error: str, details: str | None = None) -> None:
        """Display an error message."""
        self._console.print(f"❌ {error}", style="error")
        if details:
            self._console.print(f"   {details}", style="dim")
    
    def show_warning(self, warning: str) -> None:
        """Display a warning."""
        self._console.print(f"⚠️  {warning}", style="warning")
    
    def show_info(self, info: str) -> None:
        """Display info message."""
        self._console.print(f"ℹ️  {info}", style="info")
    
    def show_markdown(self, content: str) -> None:
        """Render and display markdown."""
        md = Markdown(content, code_theme=self._config.code_theme)
        self._console.print(md)
    
    def show_code(self, code: str, language: str | None = None) -> None:
        """Display syntax-highlighted code."""
        syntax = Syntax(
            code,
            language or "text",
            theme=self._config.code_theme,
            line_numbers=True,
            word_wrap=True,
        )
        self._console.print(syntax)
    
    def show_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        title: str | None = None,
    ) -> None:
        """Display a formatted table."""
        table = Table(title=title, show_header=True, header_style="bold")
        
        for header in headers:
            table.add_column(header)
        
        for row in rows:
            table.add_row(*row)
        
        self._console.print(table)
    
    def show_spinner(self, message: str) -> "RichSpinnerContext":
        """Create spinner context manager."""
        return RichSpinnerContext(self._console, message, self._config.spinner_style)
    
    def spinner(self, message: str) -> "RichSpinnerContext":
        """Create spinner context manager (alias for show_spinner)."""
        return self.show_spinner(message)
    
    def clear(self) -> None:
        """Clear terminal."""
        self._console.clear()
    
    def show_welcome(self) -> None:
        """Display welcome banner."""
        panel = Panel(
            "[bold]Cato[/bold] - Chat at the Terminal Orchestrator\n"
            "Type [cyan]/help[/cyan] for commands, [cyan]/exit[/cyan] to quit",
            title="Welcome",
            border_style="dim",
        )
        self._console.print(panel)
    
    def show_context_full(self, context_items: list[str]) -> None:
        """
        Display full context excerpts.
        
        Parameters
        ----------
        context_items : list[str]
            Context items to display.
        """
        if not context_items:
            return
        
        context_text = "\n\n[dim]---[/dim]\n\n".join([
            f"[cyan]Context {i+1}:[/cyan]\n{item}"
            for i, item in enumerate(context_items)
        ])
        
        panel = Panel(
            context_text,
            title="📚 Retrieved Context",
            border_style="cyan",
            padding=(1, 2),
        )
        self._console.print(panel)
        self._console.print()  # Add spacing
    
    def show_context_summary(self, count: int) -> None:
        """
        Display context count summary.
        
        Parameters
        ----------
        count : int
            Number of context items retrieved.
        """
        if count > 0:
            self._console.print(
                f"[dim cyan]📚 Retrieved {count} context item{'s' if count != 1 else ''}[/dim cyan]"
            )
            self._console.print()  # Add spacing


class RichSpinnerContext:
    """Context manager for loading spinner."""
    
    def __init__(self, console: Console, message: str, style: str) -> None:
        self._console = console
        self._message = message
        self._style = style
        self._live: Live | None = None
    
    def __enter__(self) -> "RichSpinnerContext":
        spinner = Spinner(self._style, text=self._message)
        self._live = Live(spinner, console=self._console, refresh_per_second=10)
        self._live.__enter__()
        return self
    
    def __exit__(self, *args: Any) -> None:
        if self._live:
            self._live.__exit__(*args)
    
    def update(self, message: str) -> None:
        """Update spinner message."""
        if self._live:
            self._live.update(Spinner(self._style, text=message))

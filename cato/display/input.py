"""Input handling with prompt_toolkit."""

import logging
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from cato.core.config import DisplayConfig

logger = logging.getLogger(__name__)


class InputHandler:
    """
    Handle user input with prompt_toolkit.
    
    Parameters
    ----------
    config : DisplayConfig
        Display configuration.
    history_path : Path
        Path to history file.
    """
    
    def __init__(self, config: DisplayConfig, history_path: Path) -> None:
        self._config = config
        
        # Create history file parent directory
        history_path = Path(history_path)
        history_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Custom key bindings
        bindings = KeyBindings()
        
        @bindings.add("c-c")
        def _(event):  # type: ignore
            """Handle Ctrl+C gracefully."""
            event.app.exit(result=None)
        
        @bindings.add("c-d")
        def _(event):  # type: ignore
            """Handle Ctrl+D for exit."""
            raise EOFError()
        
        # Create session
        self._session: PromptSession[str] = PromptSession(
            history=FileHistory(str(history_path)),
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=bindings,
            style=self._get_style(),
            multiline=False,
            enable_history_search=True,
        )
    
    def _get_style(self) -> Style:
        """Get prompt style based on theme."""
        if self._config.prompt_style or self._config.input_style:
            return Style.from_dict({
                "prompt": self._config.prompt_style or "cyan bold",
                "": self._config.input_style or "",
            })
        
        # Theme-specific styles
        if self._config.theme == "gruvbox-dark":
            return Style.from_dict({
                "prompt": "#83a598 bold",
                "": "#ebdbb2",
            })
        
        return Style.from_dict({
            "prompt": "cyan bold",
            "": "",
        })
    
    async def get_input(self, prompt: str | None = None) -> str | None:
        """
        Get user input.
        
        Parameters
        ----------
        prompt : str | None, optional
            Prompt string. Uses configured prompt symbol if None.
        
        Returns
        -------
        str | None
            User input or None if cancelled (Ctrl+C/Ctrl+D).
        """
        try:
            return await self._session.prompt_async(prompt or self._config.prompt_symbol)
        except (EOFError, KeyboardInterrupt):
            return None
    
    async def get_multiline_input(self, prompt: str | None = None) -> str | None:
        """
        Get multiline input (ends with blank line).
        
        Parameters
        ----------
        prompt : str | None, optional
            Prompt string.
        
        Returns
        -------
        str | None
            Combined input or None if cancelled.
        """
        lines = []
        continuation = "... "
        
        try:
            while True:
                base_prompt = prompt or self._config.prompt_symbol
                p = base_prompt if not lines else continuation
                line = await self._session.prompt_async(p)
                
                if not line and lines:
                    break
                lines.append(line)
            
            return "\n".join(lines)
        except (EOFError, KeyboardInterrupt):
            return None

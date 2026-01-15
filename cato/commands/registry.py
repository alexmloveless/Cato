"""Command registration system."""

import logging
from typing import Any, Callable, Type

logger = logging.getLogger(__name__)

# Global command registry
_COMMANDS: dict[str, Type[Any]] = {}
_ALIASES: dict[str, str] = {}  # alias -> primary name


def command(
    name: str,
    aliases: list[str] | None = None,
    description: str = "",
    usage: str = "",
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorator to register a command class.
    
    Parameters
    ----------
    name : str
        Primary command name (without slash).
    aliases : list[str] | None, optional
        Alternative names.
    description : str, optional
        Brief description for help.
    usage : str, optional
        Usage pattern string.
    
    Returns
    -------
    Callable
        Decorator that registers the class.
    
    Examples
    --------
    >>> @command("help", aliases=["h", "?"], description="Show help")
    ... class HelpCommand:
    ...     async def execute(self, args, context):
    ...         ...
    """
    def decorator(cls: Type[Any]) -> Type[Any]:
        # Attach metadata to class
        cls._cmd_name = name
        cls._cmd_aliases = aliases or []
        cls._cmd_description = description
        cls._cmd_usage = usage
        
        # Register
        _COMMANDS[name] = cls
        for alias in (aliases or []):
            _ALIASES[alias] = name
        
        logger.debug(f"Registered command: {name} (aliases: {aliases or []})")
        return cls
    return decorator


class CommandRegistry:
    """
    Central registry for command lookup and execution.
    
    Commands are discovered automatically when their modules are imported.
    """
    
    def __init__(self) -> None:
        self._commands = _COMMANDS
        self._aliases = _ALIASES
    
    def get(self, name: str) -> Type[Any] | None:
        """
        Look up a command by name or alias.
        
        Parameters
        ----------
        name : str
            Command name (with or without slash).
        
        Returns
        -------
        Type[Any] | None
            Command class if found.
        """
        # Strip leading slash if present
        name = name.lstrip("/")
        
        # Check aliases first
        if name in self._aliases:
            name = self._aliases[name]
        
        return self._commands.get(name)
    
    def list_commands(self) -> list[tuple[str, str, list[str]]]:
        """
        List all registered commands.
        
        Returns
        -------
        list[tuple[str, str, list[str]]]
            List of (name, description, aliases) tuples.
        """
        return [
            (name, cls._cmd_description, cls._cmd_aliases)
            for name, cls in sorted(self._commands.items())
        ]
    
    def resolve_alias(self, name: str) -> str:
        """
        Resolve an alias to its primary command name.
        
        Parameters
        ----------
        name : str
            Command name or alias.
        
        Returns
        -------
        str
            Primary command name.
        """
        return self._aliases.get(name.lstrip("/"), name.lstrip("/"))

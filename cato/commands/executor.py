"""Command execution with context and error handling."""

import logging
from typing import Callable

from cato.commands.base import CommandContext, CommandResult
from cato.commands.parser import parse_command_input
from cato.commands.registry import CommandRegistry
from cato.core.exceptions import (
    CatoError,
    CommandExecutionError,
    CommandNotFoundError,
)

logger = logging.getLogger(__name__)


class CommandExecutor:
    """
    Executes commands with proper context and error handling.
    
    Parameters
    ----------
    registry : CommandRegistry
        Command registry for lookup.
    context_factory : Callable[[], CommandContext]
        Factory function that creates command context.
    """
    
    def __init__(
        self,
        registry: CommandRegistry,
        context_factory: Callable[[], CommandContext],
    ) -> None:
        self._registry = registry
        self._context_factory = context_factory
    
    async def execute(self, input_text: str) -> CommandResult | None:
        """
        Parse and execute a command from user input.
        
        Parameters
        ----------
        input_text : str
            Raw user input.
        
        Returns
        -------
        CommandResult | None
            Result if input was a command, None if not a command.
        
        Raises
        ------
        CommandNotFoundError
            Unknown command name.
        CommandExecutionError
            Command failed during execution.
        """
        parsed = parse_command_input(input_text)
        if parsed is None:
            return None  # Not a command
        
        command_name, args = parsed
        
        # Look up command
        command_cls = self._registry.get(command_name)
        if command_cls is None:
            available = [c[0] for c in self._registry.list_commands()]
            raise CommandNotFoundError(
                f"Unknown command: /{command_name}",
                context={"available": available},
            )
        
        # Create context and execute command
        context = self._context_factory()
        
        try:
            logger.info(f"Executing command: /{command_name} with args: {args}")
            # Commands are async functions, call them directly
            result = await command_cls(context, args)
            logger.debug(f"Command result: success={result.success}, message={result.message}")
            return result
        except CatoError:
            raise  # Let Cato errors propagate
        except Exception as e:
            logger.error(f"Command /{command_name} failed: {e}", exc_info=True)
            raise CommandExecutionError(
                f"Command /{command_name} failed: {e}",
                context={"command": command_name, "args": args},
            ) from e

"""Command system with decorator-based registration."""

from cato.commands.base import Command, CommandContext, CommandResult
from cato.commands.executor import CommandExecutor
from cato.commands.parser import parse_command_input
from cato.commands.registry import CommandRegistry, command

# Import command modules to trigger @command decorator registration
import cato.commands.core  # noqa: F401
import cato.commands.productivity  # noqa: F401
import cato.commands.vector  # noqa: F401
import cato.commands.web  # noqa: F401
import cato.commands.tts  # noqa: F401
import cato.commands.context  # noqa: F401

__all__ = [
    "Command",
    "CommandContext",
    "CommandResult",
    "CommandExecutor",
    "CommandRegistry",
    "command",
    "parse_command_input",
]

"""Command system with decorator-based registration."""

from cato.commands.base import Command, CommandContext, CommandResult
from cato.commands.executor import CommandExecutor
from cato.commands.parser import parse_command_input
from cato.commands.registry import CommandRegistry, command

__all__ = [
    "Command",
    "CommandContext",
    "CommandResult",
    "CommandExecutor",
    "CommandRegistry",
    "command",
    "parse_command_input",
]

# Commands Module

This module implements the slash command system with decorator-based registration.

## Components

### `base.py`
Command protocol and base types.

**Key classes:**
- `Command`: Protocol for command implementations
- `CommandContext`: Dependency injection container for commands
- `CommandResult`: Return type for command execution

### `registry.py`
Command registration and lookup.

**Key classes:**
- `CommandRegistry`: Central registry for command lookup
- `command`: Decorator for registering commands

### `parser.py`
Command input parsing.

**Functions:**
- `parse_command_input()`: Parse slash commands with shell-like quoting

### `executor.py`
Command execution with context and error handling.

**Key classes:**
- `CommandExecutor`: Executes commands with proper context

## Usage

### Defining a Command

```python
from cato.commands import command, CommandContext, CommandResult

@command("help", aliases=["h", "?"], description="Show help")
class HelpCommand:
    async def execute(self, args: list[str], context: CommandContext) -> CommandResult:
        context.display.show_info("Help information...")
        return CommandResult(success=True, message="Help displayed")
```

### Using Commands

```python
from cato.commands import CommandExecutor, CommandRegistry

registry = CommandRegistry()
executor = CommandExecutor(registry, context_factory)

result = await executor.execute("/help")
```

## Design Principles

- **Decorator-based**: Commands self-register on import
- **Protocol-based**: Commands implement `Command` protocol
- **Dependency injection**: Context provides all dependencies
- **Error mapping**: Exceptions mapped to `CommandError` hierarchy

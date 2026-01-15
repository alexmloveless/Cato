"""
Core commands for essential application functionality.

This module implements the most basic commands needed for a functional
chat client: help, exit, clear, and config display.
"""

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command


@command(name="help", aliases=["h", "?"])
async def help_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """
    Display help information about available commands.

    Usage: /help [command]

    Without arguments, shows a list of all available commands.
    With a command name, shows detailed help for that command.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : list[str]
        Command arguments (optional command name).

    Returns
    -------
    CommandResult
        Help information to display.
    """
    from cato.commands.registry import CommandRegistry

    registry = CommandRegistry.get_instance()

    # Show help for specific command
    if args:
        command_name = args[0]
        command_func = registry.get_command(command_name)
        
        if command_func is None:
            return CommandResult(
                success=False,
                message=f"Unknown command: {command_name}"
            )
        
        # Get command info
        info = registry.get_command_info(command_name)
        if info:
            help_text = f"**{info.name}**"
            if info.aliases:
                help_text += f" (aliases: {', '.join(info.aliases)})"
            help_text += f"\n\n{info.description or 'No description available.'}"
            
            return CommandResult(success=True, message=help_text)
    
    # Show list of all commands
    all_commands = registry.list_commands()
    
    help_text = """# Available Commands

## Core Commands
- **/help** (h, ?) - Show this help message
- **/exit** (quit, q) - Exit Cato
- **/clear** (cls) - Clear conversation history
- **/config** - Show current configuration

## Usage
Type a message to chat with the AI, or use `/command` to execute commands.
Use `/help <command>` for detailed help on a specific command.
"""
    
    return CommandResult(success=True, message=help_text.strip())


@command(name="exit", aliases=["quit", "q"])
async def exit_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """
    Exit the application.

    Usage: /exit

    Cleanly shuts down Cato and returns to the terminal.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : list[str]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Exit confirmation message.
    """
    # Signal the application to stop
    ctx.app.stop()
    
    return CommandResult(
        success=True,
        message="Exiting Cato..."
    )


@command(name="clear", aliases=["cls"])
async def clear_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """
    Clear the conversation history.

    Usage: /clear

    Removes all messages from the current conversation, keeping only
    the system prompt. The next message will start a fresh conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : list[str]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Confirmation message.
    """
    # Clear the conversation history
    ctx.chat_service.clear_conversation()
    
    message_count = ctx.chat_service.get_message_count()
    
    return CommandResult(
        success=True,
        message=f"Conversation cleared. Started fresh with {message_count} messages."
    )


@command(name="config", aliases=["cfg"])
async def config_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """
    Display current configuration.

    Usage: /config [section]

    Without arguments, shows key configuration values.
    With a section name (llm, display, storage), shows detailed config for that section.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : list[str]
        Optional section name.

    Returns
    -------
    CommandResult
        Configuration information.
    """
    config = ctx.config
    
    # Show specific section
    if args:
        section = args[0].lower()
        
        if section == "llm":
            info = f"""# LLM Configuration

**Provider**: {config.llm.provider}
**Model**: {config.llm.model}
**Temperature**: {config.llm.temperature}
**Max Tokens**: {config.llm.max_tokens}
**Timeout**: {config.llm.timeout_seconds}s
"""
        elif section == "display":
            info = f"""# Display Configuration

**Theme**: {config.display.theme}
**Markdown**: {'enabled' if config.display.markdown_enabled else 'disabled'}
**Code Theme**: {config.display.code_theme}
**Prompt**: {config.display.prompt_symbol}
"""
        elif section == "storage":
            info = f"""# Storage Configuration

**Database**: {config.storage.database_path}
**Backup**: {'enabled' if config.storage.backup_enabled else 'disabled'}
"""
        elif section == "commands":
            info = f"""# Commands Configuration

**Prefix**: {config.commands.prefix}
**History File**: {config.commands.history_file}
"""
        else:
            return CommandResult(
                success=False,
                message=f"Unknown config section: {section}\\n"
                        "Available sections: llm, display, storage, commands"
            )
        
        return CommandResult(success=True, message=info.strip())
    
    # Show overview
    info = f"""# Cato Configuration

**LLM Provider**: {config.llm.provider} ({config.llm.model})
**Theme**: {config.display.theme}
**Database**: {config.storage.database_path}
**Debug Mode**: {'enabled' if config.debug else 'disabled'}

Use `/config <section>` for detailed configuration.
Available sections: llm, display, storage, commands
"""
    
    return CommandResult(success=True, message=info.strip())


@command(name="info", aliases=["about"])
async def info_command(ctx: CommandContext, args: list[str]) -> CommandResult:
    """
    Display information about Cato.

    Usage: /info

    Shows version, current session stats, and system information.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : list[str]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Application information.
    """
    message_count = ctx.chat_service.get_message_count()
    
    info = f"""# Cato - Terminal LLM Chat Client

**Version**: 0.1.0
**Provider**: {ctx.chat_service.provider.name}
**Model**: {ctx.chat_service.provider.model}

**Current Session**:
- Messages: {message_count}
- Storage: {ctx.config.storage.database_path}

Cato is a terminal-first LLM chat client with conversation memory,
productivity features, and extensible command system.
"""
    
    return CommandResult(success=True, message=info.strip())

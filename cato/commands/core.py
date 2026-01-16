"""
Core commands for essential application functionality.

This module implements the most basic commands needed for a functional
chat client: help, exit, clear, and config display.
"""

import logging

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.services.help import HelpService

logger = logging.getLogger(__name__)


@command(name="help", aliases=["h", "?"])
async def help_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display help information about commands and topics.

    Usage: 
      /help                    # Show overview
      /help commands           # List all commands
      /help <topic>            # Show topic or category
      /help <command>          # Show command help
      /help model "question"   # Ask model about Cato

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Query (topic, category, or command) or 'model' with question.

    Returns
    -------
    CommandResult
        Help information to display.
    """
    # Initialize HelpService
    help_service = HelpService()
    
    # Handle /help model "question"
    if args and args[0] == "model":
        if len(args) < 2:
            return CommandResult(
                success=False,
                message="Usage: /help model \"your question\""
            )
        
        question = " ".join(args[1:])
        
        # Get all help files for context
        help_files = help_service.get_all_help_files()
        
        # Build context from help files
        context = "# Cato Help Documentation\n\n"
        for file_path, content in help_files:
            context += f"## {file_path}\n\n{content}\n\n---\n\n"
        
        # Create one-off LLM query
        try:
            from cato.core.types import Message
            
            messages = [
                Message(
                    role="system",
                    content="You are a helpful assistant for Cato, a terminal-first LLM chat client. "
                            "Answer questions strictly based on the help documentation provided. "
                            "If the answer is not in the documentation, say so."
                ),
                Message(
                    role="user",
                    content=f"{context}\n\nQuestion: {question}"
                )
            ]
            
            # Use LLM provider directly (don't add to conversation history)
            result = await ctx.llm.complete(messages=messages)
            
            return CommandResult(
                success=True,
                message=f"**Help Model Response:**\n\n{result.content}"
            )
        except Exception as e:
            logger.error(f"Failed to query help model: {e}")
            return CommandResult(
                success=False,
                message=f"Failed to query help model: {e}"
            )
    
    # Regular help query
    query = args[0] if args else None
    content = help_service.get_help_content(query)
    
    if content:
        return CommandResult(success=True, message=content)
    
    # Not found - provide suggestions
    suggestions = help_service.get_suggestions(query) if query else []
    
    error_msg = f"Help topic not found: {query}\n\n"
    if suggestions:
        error_msg += "Did you mean:\n"
        for suggestion in suggestions:
            error_msg += f"- /help {suggestion}\n"
    else:
        error_msg += "Try:\n- /help commands - List all commands\n- /help <category> - Show category commands"
    
    return CommandResult(success=False, message=error_msg.strip())


@command(name="exit", aliases=["quit", "q"])
async def exit_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Exit the application.

    Usage: /exit

    Cleanly shuts down Cato and returns to the terminal.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Exit confirmation message.
    """
    return CommandResult(
        success=True,
        message="Exiting Cato...",
        data={"should_exit": True}
    )


@command(name="clear", aliases=["cls"])
async def clear_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Clear the conversation history.

    Usage: /clear

    Removes all messages from the current conversation, keeping only
    the system prompt. The next message will start a fresh conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Confirmation message.
    """
    # TODO: Implement conversation clearing when conversation service is ready
    return CommandResult(
        success=True,
        message="Conversation clearing not yet implemented."
    )


@command(name="config", aliases=["cfg"])
async def config_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display current configuration.

    Usage: /config [section]

    Without arguments, shows key configuration values.
    With a section name (llm, display, storage), shows detailed config for that section.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
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
async def info_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display information about Cato.

    Usage: /info

    Shows version, current session stats, and system information.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
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


@command(name="loglevel", aliases=["log"])
async def loglevel_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Show or change the logging level.

    Usage:
      /loglevel              # Show current level
      /loglevel <level>      # Set level (DEBUG, INFO, WARNING, ERROR)

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional log level to set.

    Returns
    -------
    CommandResult
        Current or updated log level.
    """
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

    # Show current level
    if not args:
        current_level = logging.getLogger().level
        level_name = logging.getLevelName(current_level)

        return CommandResult(
            success=True,
            message=f"Current log level: **{level_name}**\n\n"
                   f"Available levels: {', '.join(valid_levels)}\n"
                   f"Usage: /loglevel <level>"
        )

    # Set new level
    new_level = args[0].upper()

    if new_level not in valid_levels:
        return CommandResult(
            success=False,
            message=f"Invalid log level: {new_level}\n"
                   f"Valid levels: {', '.join(valid_levels)}"
        )

    # Update logging level
    logging.getLogger().setLevel(getattr(logging, new_level))
    logger.info(f"Log level changed to {new_level}")

    return CommandResult(
        success=True,
        message=f"✓ Log level set to **{new_level}**"
    )

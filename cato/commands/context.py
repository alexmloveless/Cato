"""Context and thread management commands.

This module provides commands for managing conversation context and resuming
previous threads from the vector store.
"""

import logging

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command

logger = logging.getLogger(__name__)


@command(name="showcontext")
async def showcontext_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Toggle or set context display mode.
    
    Controls whether and how retrieved context from the vector store is
    displayed before each response. Context is always injected into prompts
    when available, but this command controls user visibility.
    
    Usage:
      /showcontext          # Toggle through modes: off -> summary -> on -> off
      /showcontext on       # Enable full context display
      /showcontext off      # Disable context display
      /showcontext summary  # Show only count of items retrieved
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Optional mode argument (on/off/summary).
    
    Returns
    -------
    CommandResult
        Status of mode change.
    
    Notes
    -----
    - Requires vector store to be enabled
    - Mode persists for the duration of the session
    - "off": Context injected but not shown (default)
    - "summary": Show count of context items only
    - "on": Display full context excerpts
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Context display requires vector store to be enabled. "
                   "Configure vector_store.enabled=true in your config."
        )
    
    # Determine new mode
    if args:
        mode = args[0].lower()
        if mode not in ["on", "off", "summary"]:
            return CommandResult(
                success=False,
                message="Invalid mode. Use: on, off, or summary"
            )
    else:
        # Toggle through modes
        modes = ["off", "summary", "on"]
        current_idx = modes.index(ctx.chat.context_display_mode)
        mode = modes[(current_idx + 1) % len(modes)]
    
    # Update mode
    ctx.chat.context_display_mode = mode
    
    # Build descriptive message
    descriptions = {
        "off": "Context is injected into prompts but not displayed",
        "summary": "Context count will be shown before responses",
        "on": "Full context excerpts will be displayed before responses"
    }
    
    return CommandResult(
        success=True,
        message=f"✓ Context display: {mode}\n{descriptions[mode]}"
    )


@command(name="continue", aliases=["cont"])
async def continue_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Resume a previous conversation thread.

    Loads all message exchanges from a specific session/thread ID and
    reconstructs the conversation history. This allows continuing
    conversations from previous sessions.

    Usage:
      /continue <session_id>    # Resume thread by session ID

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Session ID to continue.

    Returns
    -------
    CommandResult
        Status of thread continuation.

    Notes
    -----
    - Requires vector store to be enabled
    - Clears current conversation and replaces with loaded thread
    - Session ID can be found in vector store metadata or previous logs
    """
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /continue <session_id>"
        )

    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Thread continuation requires vector store to be enabled. "
                   "Configure vector_store.enabled=true in your config."
        )

    session_id = args[0]

    try:
        # Use chat service to load thread
        exchange_count = await ctx.chat.continue_thread(session_id)

        if exchange_count == 0:
            return CommandResult(
                success=False,
                message=f"No conversation found for session: {session_id}"
            )

        return CommandResult(
            success=True,
            message=f"✓ Loaded {exchange_count} message exchange(s) from session: {session_id}\n"
                   f"You can now continue the conversation from where it left off."
        )

    except ValueError as e:
        logger.error(f"Thread continuation failed: {e}")
        return CommandResult(
            success=False,
            message=f"Cannot continue thread: {e}"
        )
    except Exception as e:
        logger.error(f"Failed to continue thread: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to continue thread: {e}"
        )

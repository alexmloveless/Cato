"""
Context and thread management commands.

This module provides commands for managing conversation context and resuming
previous threads from the vector store.
"""

import logging

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command

logger = logging.getLogger(__name__)


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

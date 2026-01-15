"""Command input parsing."""

import logging
import shlex

logger = logging.getLogger(__name__)


def parse_command_input(input_text: str) -> tuple[str, list[str]] | None:
    """
    Parse user input into command name and arguments.
    
    Parameters
    ----------
    input_text : str
        Raw user input.
    
    Returns
    -------
    tuple[str, list[str]] | None
        (command_name, args) if input is a command, None otherwise.
    
    Examples
    --------
    >>> parse_command_input("/help")
    ("help", [])
    >>> parse_command_input('/web "search query" google')
    ("web", ["search query", "google"])
    >>> parse_command_input("hello")
    None
    """
    text = input_text.strip()
    
    # Must start with /
    if not text.startswith("/"):
        return None
    
    # Remove leading slash
    text = text[1:]
    
    # Handle empty command
    if not text:
        return None
    
    try:
        # Use shlex for shell-like tokenization
        tokens = shlex.split(text)
    except ValueError as e:
        # Unbalanced quotes - treat rest as single argument
        logger.warning(f"Failed to parse command input: {e}")
        parts = text.split(maxsplit=1)
        tokens = [parts[0], parts[1]] if len(parts) > 1 else [parts[0]]
    
    command_name = tokens[0].lower()
    args = tokens[1:] if len(tokens) > 1 else []
    
    return (command_name, args)

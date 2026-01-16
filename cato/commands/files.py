"""File operation commands for reading and attaching files."""

import logging
import os
from pathlib import Path

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command

logger = logging.getLogger(__name__)


def resolve_file_path(path_str: str, locations: dict[str, str]) -> Path:
    """
    Resolve file path with location alias support.

    Parameters
    ----------
    path_str : str
        Path string, possibly with alias prefix (e.g., "docs:notes.txt").
    locations : dict[str, str]
        Location aliases from config.

    Returns
    -------
    Path
        Resolved absolute path.

    Examples
    --------
    >>> resolve_file_path("docs:notes.txt", {"docs": "~/Documents"})
    Path('/home/user/Documents/notes.txt')
    >>> resolve_file_path("/absolute/path.txt", {})
    Path('/absolute/path.txt')
    """
    # Check for alias prefix (e.g., "docs:notes.txt")
    if ":" in path_str:
        alias, filename = path_str.split(":", 1)
        if alias in locations:
            base_path = Path(locations[alias]).expanduser()
            return base_path / filename

    # No alias, treat as regular path
    return Path(path_str).expanduser().resolve()


def is_text_file(file_path: Path) -> bool:
    """
    Check if file appears to be a text file.

    Parameters
    ----------
    file_path : Path
        Path to file to check.

    Returns
    -------
    bool
        True if file appears to be text, False if binary.
    """
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            # Check for null bytes (common in binary files)
            if b"\x00" in chunk:
                return False
            # Try to decode as UTF-8
            try:
                chunk.decode("utf-8")
                return True
            except UnicodeDecodeError:
                return False
    except Exception:
        return False


@command(
    name="attach",
    description="Attach file contents as conversation context",
    usage="/attach <file1> [file2] [file3] ... (max 5 files)",
    aliases=["a"],
)
async def attach_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Attach file contents to conversation.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        File paths to attach (supports location aliases).

    Returns
    -------
    CommandResult
        Result with attached file contents or error.
    """
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /attach <file1> [file2] [file3] ... (max 5 files)\n"
                   "Example: /attach notes.txt docs:readme.md"
        )

    # Validate number of files
    if len(args) > 5:
        return CommandResult(
            success=False,
            message="Maximum 5 files can be attached at once."
        )

    locations = ctx.config.locations
    attached_files = []
    errors = []

    # Process each file
    for file_arg in args:
        try:
            # Resolve path (with alias support)
            file_path = resolve_file_path(file_arg, locations)

            # Check if file exists
            if not file_path.exists():
                errors.append(f"File not found: {file_arg}")
                continue

            # Check if it's a file (not directory)
            if not file_path.is_file():
                errors.append(f"Not a file: {file_arg}")
                continue

            # Check if it's a text file
            if not is_text_file(file_path):
                errors.append(f"Binary file rejected: {file_arg}")
                continue

            # Check permissions
            if not os.access(file_path, os.R_OK):
                errors.append(f"Permission denied: {file_arg}")
                continue

            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"Failed to read {file_arg}: {e}")
                continue

            # Add to attached files list
            attached_files.append({
                "name": file_path.name,
                "path": str(file_path),
                "content": content,
            })

        except Exception as e:
            logger.error(f"Error processing file {file_arg}: {e}")
            errors.append(f"Error processing {file_arg}: {e}")

    # If no files were successfully attached
    if not attached_files:
        error_msg = "No files were attached.\n\n"
        if errors:
            error_msg += "Errors:\n"
            for error in errors:
                error_msg += f"- {error}\n"
        return CommandResult(
            success=False,
            message=error_msg.strip()
        )

    # Format attached content as user message
    formatted_content = "[Attached Files]\n\n"
    for file in attached_files:
        formatted_content += f"--- File: {file['name']} ---\n"
        formatted_content += f"Path: {file['path']}\n\n"
        formatted_content += file['content']
        formatted_content += "\n\n"

    # Add to conversation history
    ctx.chat_service.conversation.add_user_message(formatted_content.strip())

    # Build success message
    success_msg = f"✓ Attached {len(attached_files)} file(s):\n"
    for file in attached_files:
        success_msg += f"- {file['name']}\n"

    if errors:
        success_msg += "\nWarnings:\n"
        for error in errors:
            success_msg += f"- {error}\n"

    # Prompt for vector store addition (if vector store is enabled)
    if ctx.vector_store is not None:
        success_msg += "\n💡 Tip: Use /vdoc to add these files to the vector store for future reference."

    return CommandResult(
        success=True,
        message=success_msg.strip()
    )


@command(
    name="locations",
    description="Show configured location aliases",
    usage="/locations",
    aliases=["locs"],
)
async def locations_command(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display configured location aliases.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Command arguments (unused).

    Returns
    -------
    CommandResult
        Result with location aliases listing.
    """
    locations = ctx.config.locations

    if not locations:
        return CommandResult(
            success=True,
            message="No location aliases configured.\n\n"
                   "Add aliases to your config.yaml:\n"
                   "```yaml\n"
                   "locations:\n"
                   "  docs: ~/Documents\n"
                   "  projects: ~/Code/projects\n"
                   "```"
        )

    # Format locations
    msg = "# Location Aliases\n\n"
    for alias, path in sorted(locations.items()):
        resolved_path = Path(path).expanduser()
        msg += f"**{alias}**: `{path}`\n"
        if resolved_path.exists():
            msg += f"  → {resolved_path}\n"
        else:
            msg += f"  → {resolved_path} ⚠️  (does not exist)\n"
        msg += "\n"

    msg += "**Usage**: `/attach docs:notes.txt` or `/vdoc projects:readme.md`"

    return CommandResult(
        success=True,
        message=msg.strip()
    )

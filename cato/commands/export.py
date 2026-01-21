"""Export commands for saving conversation content to files or clipboard."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from cato.commands.base import CommandContext, CommandResult
from cato.commands.files import resolve_file_path
from cato.commands.registry import command


def _resolve_output_path(ctx: CommandContext, path_str: str) -> Path:
    """Resolve a destination path using location aliases and ~ expansion.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    path_str : str
        Destination path string.

    Returns
    -------
    Path
        Resolved output path.
    """
    locations = ctx.config.locations or {}
    return resolve_file_path(path_str, locations)


def _write_text_atomic(path: Path, content: str) -> None:
    """Write text to a file, creating parent directories.

    Notes
    -----
    Uses a simple atomic replace to avoid partially-written files.

    Parameters
    ----------
    path : Path
        Destination file path.
    content : str
        Text content to write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.with_name(f".{path.name}.tmp")
    tmp_path.write_text(content, encoding="utf-8")
    tmp_path.replace(path)


def _get_conversation_messages(ctx: CommandContext) -> list[dict[str, Any]]:
    """Return the conversation as a normalized list of message dicts.

    Parameters
    ----------
    ctx : CommandContext
        Command execution context.

    Returns
    -------
    list[dict[str, Any]]
        Messages in chronological order with keys: role, content, timestamp.
    """
    conversation = getattr(ctx, "conversation", None) or getattr(ctx.chat, "conversation", None)
    if conversation is None:
        return []

    messages: list[dict[str, Any]] = []

    system_prompt = getattr(conversation, "system_prompt", None)
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt, "timestamp": None})

    for msg in getattr(conversation, "messages", []) or []:
        messages.append(
            {
                "role": getattr(msg, "role", "unknown"),
                "content": getattr(msg, "content", str(msg)),
                "timestamp": getattr(msg, "timestamp", None),
            }
        )

    return messages


def _get_last_exchange(ctx: CommandContext) -> tuple[str | None, str | None]:
    """Return (user_message, assistant_message) for the most recent exchange."""
    user_msg: str | None = None
    assistant_msg: str | None = None

    for msg in reversed(_get_conversation_messages(ctx)):
        if msg["role"] == "assistant" and assistant_msg is None:
            assistant_msg = msg["content"]
            continue

        if msg["role"] == "user" and assistant_msg is not None:
            user_msg = msg["content"]
            break

    return user_msg, assistant_msg


def _extract_code_blocks(markdown_text: str) -> list[str]:
    """Extract fenced code blocks from markdown.

    Supports opening fences with optional language identifiers and metadata,
    e.g.:

    ```python path=/some/file.py start=10
    print('hi')
    ```

    Parameters
    ----------
    markdown_text : str
        Markdown text.

    Returns
    -------
    list[str]
        Code block contents.
    """
    pattern = r"```[^\n]*\n(.*?)```"
    return re.findall(pattern, markdown_text, flags=re.DOTALL)


@command(name="writecode", aliases=["wcode"])
async def writecode_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Extract code blocks from the last assistant response and write to file."""
    if not args:
        return CommandResult(success=False, message="Usage: /writecode <output_file>")

    output_path = _resolve_output_path(ctx, args[0])
    _, assistant_msg = _get_last_exchange(ctx)

    if not assistant_msg:
        return CommandResult(success=False, message="No assistant response to extract code from")

    blocks = _extract_code_blocks(assistant_msg)
    if not blocks:
        return CommandResult(success=False, message="No code blocks found in last response")

    combined = "\n\n".join(blocks)

    try:
        _write_text_atomic(output_path, combined)
    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Write failed: {e}")

    return CommandResult(
        success=True,
        message=f"Extracted {len(blocks)} code block(s) to {output_path}",
    )


@command(name="writejson", aliases=["wjson"])
async def writejson_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Export the full conversation to JSON."""
    if not args:
        return CommandResult(success=False, message="Usage: /writejson <output_file>")

    output_path = _resolve_output_path(ctx, args[0])
    messages = _get_conversation_messages(ctx)

    if not messages:
        return CommandResult(success=False, message="No conversation to export")

    export_data = {
        "conversation": messages,
        "config": {
            "model": getattr(ctx.config.llm, "model", None),
            "temperature": getattr(ctx.config.llm, "temperature", None),
            "max_tokens": getattr(ctx.config.llm, "max_tokens", None),
        },
    }

    try:
        _write_text_atomic(
            output_path,
            json.dumps(export_data, indent=2, ensure_ascii=False),
        )
    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Write failed: {e}")

    return CommandResult(success=True, message=f"Exported {len(messages)} messages to {output_path}")


@command(name="writemd", aliases=["w"])
async def writemd_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Export conversation to Markdown (excluding system prompt)."""
    if not args:
        return CommandResult(success=False, message="Usage: /writemd <output_file>")

    output_path = _resolve_output_path(ctx, args[0])

    messages = [m for m in _get_conversation_messages(ctx) if m["role"] in ("user", "assistant")]
    if not messages:
        return CommandResult(success=False, message="No conversation to export")

    lines: list[str] = ["# Thread Export", "", f"**Model:** {ctx.config.llm.model}", f"**Temperature:** {ctx.config.llm.temperature}", "", "---", ""]

    for msg in messages:
        role = msg["role"].capitalize()
        lines.append(f"## {role}")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
        lines.append("---")
        lines.append("")

    try:
        _write_text_atomic(output_path, "\n".join(lines).rstrip() + "\n")
    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Write failed: {e}")

    return CommandResult(success=True, message=f"Exported to {output_path}")


@command(name="writemdall", aliases=["wmdall"])
async def writemdall_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Export conversation to Markdown including system prompt."""
    if not args:
        return CommandResult(success=False, message="Usage: /writemdall <output_file>")

    output_path = _resolve_output_path(ctx, args[0])
    messages = _get_conversation_messages(ctx)

    if not messages:
        return CommandResult(success=False, message="No conversation to export")

    lines: list[str] = [
        "# Full Conversation Export",
        "",
        f"**Model:** {ctx.config.llm.model}",
        f"**Temperature:** {ctx.config.llm.temperature}",
        "",
        "---",
        "",
    ]

    for msg in messages:
        role = msg["role"].capitalize()
        lines.append(f"## {role}")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
        lines.append("---")
        lines.append("")

    try:
        _write_text_atomic(output_path, "\n".join(lines).rstrip() + "\n")
    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Write failed: {e}")

    return CommandResult(success=True, message=f"Exported to {output_path}")


@command(name="writeresp", aliases=["wresp"])
async def writeresp_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Export the last exchange to a file in text, JSON, or Markdown format."""
    if not args:
        return CommandResult(success=False, message="Usage: /writeresp <output_file> [json|md]")

    output_path = _resolve_output_path(ctx, args[0])
    format_type = args[1].lower() if len(args) > 1 else "text"

    user_msg, assistant_msg = _get_last_exchange(ctx)
    if not assistant_msg:
        return CommandResult(success=False, message="No exchange to export")

    if format_type == "json":
        payload = {
            "user": user_msg,
            "assistant": assistant_msg,
            "timestamp": datetime.now().isoformat(),
        }
        content = json.dumps(payload, indent=2, ensure_ascii=False)
    elif format_type == "md":
        content = (
            f"## User\n\n{user_msg or '(no user message)'}\n\n---\n\n"
            f"## Assistant\n\n{assistant_msg}\n"
        )
    else:
        if user_msg:
            content = f"User:\n{user_msg}\n\nAssistant:\n{assistant_msg}\n"
        else:
            content = assistant_msg + "\n"

    try:
        _write_text_atomic(output_path, content)
    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Write failed: {e}")

    return CommandResult(success=True, message=f"Exported last exchange to {output_path}")


@command(name="append")
async def append_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Append last exchange or custom text to a file."""
    if not args:
        return CommandResult(success=False, message="Usage: /append <file> [text]")

    output_path = _resolve_output_path(ctx, args[0])

    if len(args) > 1:
        content = " ".join(args[1:]).strip('"').strip("'")
    else:
        user_msg, assistant_msg = _get_last_exchange(ctx)
        if not assistant_msg:
            return CommandResult(success=False, message="No exchange to append")

        content = (
            "---\n\n"
            f"User:\n{user_msg or '(no user message)'}\n\n"
            f"Assistant:\n{assistant_msg}\n"
        )

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists():
            # Ensure a newline boundary (avoid gluing onto last line).
            existing_tail = output_path.read_bytes()[-1:]  # empty if file is empty
            if existing_tail and existing_tail != b"\n":
                content = "\n" + content

        with output_path.open("a", encoding="utf-8") as f:
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")

    except PermissionError:
        return CommandResult(success=False, message=f"Permission denied: {output_path}")
    except OSError as e:
        return CommandResult(success=False, message=f"Append failed: {e}")

    return CommandResult(success=True, message=f"Appended to {output_path}")


@command(name="copy")
async def copy_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Copy last assistant response to the system clipboard."""
    _ = args  # unused

    _, assistant_msg = _get_last_exchange(ctx)
    if not assistant_msg:
        return CommandResult(success=False, message="No assistant response to copy")

    if shutil.which("wl-copy") is not None:
        cmd: list[str] | None = ["wl-copy"]
    elif shutil.which("xclip") is not None:
        cmd = ["xclip", "-selection", "clipboard"]
    elif shutil.which("xsel") is not None:
        cmd = ["xsel", "--clipboard", "--input"]
    elif shutil.which("pbcopy") is not None:
        cmd = ["pbcopy"]
    elif shutil.which("clip") is not None:
        cmd = ["clip"]
    else:
        cmd = None

    if cmd is None:
        return CommandResult(
            success=False,
            message="No clipboard utility found. Install wl-clipboard, xclip, or xsel.",
        )

    try:
        # Use text mode so platform-specific encoding is handled by Python.
        subprocess.run(cmd, input=assistant_msg, text=True, check=True)
    except Exception as e:
        return CommandResult(success=False, message=f"Failed to copy to clipboard: {e}")

    return CommandResult(success=True, message="Copied last response to clipboard")

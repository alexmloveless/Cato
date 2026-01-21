# Export Commands Technical Specification

## Overview
This document specifies implementation details for the export-oriented commands defined in `Project/Spec/functional/SPEC_FILE_OPERATIONS.md`:
- `/writecode`
- `/writejson`
- `/writemd` and alias `/w`
- `/writemdall`
- `/writeresp`
- `/append`
- `/copy`

These commands export content from the current conversation (or last exchange/response) to files or the system clipboard.

## Goals
- Deterministic export behavior aligned with the functional spec.
- Local-only behavior (no network access).
- Minimal MVP implementation that matches the command framework.

## Non-Goals
- No templating or multi-file project generation.
- No git integration.
- No advanced Markdown parsing beyond fenced code block extraction.

## Code Location
- Commands live in `cato/commands/export.py`.
- `cato/commands/__init__.py` must import `cato.commands.export` so the decorator registration runs.

## Inputs and Data Sources
The export commands depend on the active conversation.

### Conversation access
Use, in order:
- `ctx.conversation` (preferred)
- `ctx.chat.conversation` (fallback)

### Normalized message representation
For export, messages are normalized to:
- `role`: string (system/user/assistant)
- `content`: string
- `timestamp`: null (until timestamps are implemented)

## Path Resolution
Exports must support the location alias scheme from `SPEC_FILE_OPERATIONS.md`.

- Use `cato/commands/files.py:resolve_file_path` with `ctx.config.locations`.
- `~` expansion is supported.

## File Writing
- All file writes use UTF-8.
- `/write*` commands overwrite the destination.
- `/append` appends (creating the file if needed).

### Atomic writes
For overwrite operations, write to a temporary sibling file and then replace the final path.

## Command Behaviors

### /writecode
- Extract fenced code blocks from the last assistant response.
- Supports opening fences that include metadata (e.g. `python path=... start=...`).
- Concatenate extracted blocks with a blank line between them.

### /writejson
- Export the full conversation to JSON:
  - `conversation`: normalized messages
  - `config`: minimal LLM config snapshot (model, temperature, max_tokens)

### /writemd and /w
- Export user+assistant messages only.
- Exclude system prompt.

### /writemdall
- Export all messages including system prompt.

### /writeresp
- Export only the last exchange.
- Format selection:
  - no format arg => plain text
  - `json` => JSON
  - `md` => Markdown

### /append
- If text argument provided: append that text.
- Otherwise: append a formatted representation of the last exchange.
- Ensure a newline boundary when appending to non-empty files.

### /copy
- Copy the last assistant response.
- Prefer common clipboard utilities:
  - `wl-copy` (Wayland)
  - `xclip`
  - `xsel`
  - `pbcopy`
  - `clip`
- If none are available, return an actionable error message.

## Errors and UX
- Missing args => `CommandResult(success=False, message="Usage: ...")`.
- No conversation/response available => clear error.
- I/O failures => include the resolved destination path in the error message.

## Help System Requirements
Per `TECH_HELP_SYSTEM.md`:
- Add help pages in `cato/resources/help/commands/` for each command.
- Add entries in `cato/resources/help/index.yaml` under an `export` category.
- Update `cato/resources/help/topics/commands.md` to list export commands.

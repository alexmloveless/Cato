# Help System Functional Specification

## Overview
The help system provides comprehensive, easy-to-navigate documentation for all commands and key workflows within Cato. Help content must be consistent, concise, and complete, so users can quickly find how to use any command.

## Goals
- Provide an **extensive yet concise** help section covering every command.
- Make help **easy to navigate** with predictable topics and command lookups.
- Ensure help content is the **single source of truth** for in-app documentation.
- Require agents adding new commands to **update help documentation** immediately.

## User-Facing Behavior

### /help (overview)
Shows a high-level index of help topics and how to navigate:
- How to list all commands
- How to view a category
- How to view a single command
- How to ask the model using help docs

### /help commands
Shows **all commands** grouped by category with brief one-line summaries.

### /help <category>
Shows all commands in a category with one-line summaries and usage hints.

### /help <command>
Shows a focused help page for a single command, including:
- Purpose and short description
- Usage
- Arguments/options
- Examples
- Aliases
- Related commands

### /help model "<question>"
Asks the model about Cato using **only** help documentation content. This behavior is detailed in the command system spec and must align with the help content structure defined here.

### Unknown topic or command
Return a clear error and provide suggestions:
- List of close matches
- Link back to `/help commands` and `/help <category>`

## Help Content Requirements

### Coverage
Every command in the command registry must have a help entry. No exceptions.

### Structure for Command Pages
Each command help page must follow a consistent order:
1. **Summary** (1–2 lines)
2. **Usage**
3. **Arguments/Options**
4. **Examples**
5. **Aliases**
6. **Notes** (only if needed)
7. **Related Commands**

### Style
- Keep descriptions short and actionable.
- Prefer bullets and short paragraphs.
- Avoid unnecessary jargon.
- Use consistent headings across pages.

## Update Responsibility (Non-Negotiable)
When a new command or alias is added:
- The command must be documented in the help system.
- The help index/navigation must be updated to include it.
- The command must appear in `/help commands` and its category list.

Failure to update help documentation is considered incomplete work.

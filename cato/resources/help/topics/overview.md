# Cato Help System

Welcome to Cato, a terminal-first LLM chat client with productivity features.

## Quick Start

- **Chat**: Just type your message and press Enter
- **Commands**: Start with `/` to execute commands (e.g., `/help`, `/clear`, `/exit`)
- **History**: Use `/history` to view past exchanges
- **Tasks**: Use `/st` to view tasks
- **Lists**: Use `/list` to view lists, `/add` to add items, `/done` to mark complete

## Getting Help

### View All Commands
```
/help commands
```
Shows all available commands organized by category.

### View Command Help
```
/help <command>
```
Shows detailed help for a specific command.
Examples: `/help st`, `/help vquery`

### View Category Help
```
/help <category>
```
Shows all commands in a category.
Categories: core, history, vector, productivity

### Ask the Model
```
/help model "your question"
```
Ask the LLM about Cato functionality using help documentation as context.
This does not add to conversation history.

## Command Categories

- **Core**: Essential commands (help, exit, clear, config)
- **History & Context**: Conversation management (history, delete, model, showsys)
- **Vector Store**: Semantic memory (vadd, vdoc, vquery, vstats)
- **Productivity**: Task and list management (st, list)

## Configuration

View current configuration with `/config`.
Edit `~/.config/cato/config.yaml` to customize settings.

## More Information

For detailed documentation on specific features:
- `/help vector` - Vector store and semantic search
- `/help productivity` - Task and list management
- `/help commands` - Complete command reference

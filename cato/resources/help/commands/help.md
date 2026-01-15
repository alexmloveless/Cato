# /help

Show help information for commands and topics.

## Usage

```
/help                    # Show help overview
/help commands           # List all commands
/help <category>         # Show commands in category
/help <command>          # Show command help
/help model "question"   # Ask model about Cato
```

## Arguments

- `topic|command` (optional) - Topic, category, or command name to show help for

## Examples

```
/help                    # Show overview
/help commands           # List all commands  
/help vector             # Show vector store commands
/help st                 # Show /st command help
/help model "how do I filter tasks by priority?"
```

## Categories

- `core` - Essential commands
- `history` - History and context management
- `vector` - Vector store operations
- `productivity` - Task and list management

## Related Commands

- `/config` - Show current configuration

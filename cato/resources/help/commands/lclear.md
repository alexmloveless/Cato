# /lclear

Clear items from a list. Can remove all items or only items with a specific status.

## Usage

```
/lclear <list> [options]
```

## Arguments

- `list` (required) - Name of the list to clear

## Options

- `-S, --status <status>` - Only clear items with this status: pending, active, in_progress, done
- `-f, --force` - Skip confirmation prompt (required when clearing all items or multiple items)

## Examples

```
/lclear todo -S done            # Remove all completed items from todo list
/lclear shopping -S done -f     # Remove completed items without confirmation
/lclear old_list -f             # Remove all items from list (requires -f)
```

## Notes

- Clearing items with a specific status (e.g., `-S done`) does not require `-f` flag
- Clearing all items (no status specified) requires `-f` flag for confirmation
- The list itself is not deleted, only the items
- Use `/delete-list` to remove the list entirely

## Aliases

- `/lclean`

## Related Commands

- `/list` - Display items in list
- `/remove` - Remove single item
- `/delete-list` - Delete entire list including all items
- `/done` - Mark items as complete before clearing

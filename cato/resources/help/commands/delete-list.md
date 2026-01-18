# /delete-list

Delete an entire list and all its items.

## Usage

```
/delete-list <name> [options]
```

## Arguments

- `name` (required) - Name of the list to delete

## Options

- `-f, --force` - Skip confirmation prompt (required if list contains items)

## Examples

```
/delete-list old_list           # Attempt to delete list (fails if it has items)
/delete-list old_list -f        # Delete list and all items without confirmation
/delete-list todo -f            # Force delete todo list and all its items
```

## Notes

- If the list contains items, the `-f` flag is required
- This permanently deletes the list and all its items
- Empty lists can be deleted without the `-f` flag
- There is no undo operation

## Aliases

- `/dl`
- `/rmlist`

## Related Commands

- `/lists` - Show all lists
- `/list` - Display items in a list
- `/lclear` - Clear items from list (keeps the list)
- `/remove` - Remove single item

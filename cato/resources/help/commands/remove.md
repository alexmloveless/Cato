# /remove

Remove an item from a list by its ID.

## Usage

```
/remove <id>
```

## Arguments

- `id` (required) - The item ID to remove (e.g., 1, 42, 123)

## Examples

```
/remove 1                       # Remove item #001
/remove 42                      # Remove item #042
```

## Notes

- Use `/list` to see item IDs
- This permanently deletes the item
- There is no confirmation prompt

## Aliases

- `/rm`
- `/del`

## Related Commands

- `/list` - Display items with IDs
- `/add` - Add new item
- `/clear` - Clear multiple items from a list
- `/done` - Mark item as complete instead of removing

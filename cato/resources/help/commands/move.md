# /move

Move an item from one list to another.

## Usage

```
/move <id> <target_list>
```

## Arguments

- `id` (required) - The item ID to move
- `target_list` (required) - Name of the destination list

## Examples

```
/move 5 shopping                # Move item #005 to shopping list
/move 12 todo                   # Move item #012 to todo list
/move 3 ideas                   # Move item #003 to ideas list
```

## Notes

- The target list is created automatically if it doesn't exist
- Item ID remains the same after moving
- All item properties (status, priority, tags, etc.) are preserved

## Aliases

- `/mv`

## Related Commands

- `/list` - Display items with IDs and list names
- `/lists` - Show all available lists
- `/add` - Add new item to a list
- `/update` - Update item fields

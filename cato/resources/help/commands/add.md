# /add

Add a new item to a list. Creates the list automatically if it doesn't exist.

## Usage

```
/add <list> <description> [options]
```

## Arguments

- `list` (required) - Name of the list to add item to
- `description` (required) - Description of the item (can be multiple words)

## Options

- `-p, --priority <level>` - Set priority: urgent, high, medium, low (default: medium)
- `-c, --category <name>` - Set category for grouping
- `-t, --tag <tags>` - Set tags (comma-separated)

## Examples

```
/add todo Complete project report
/add todo Review code -p high
/add shopping Buy milk -c groceries
/add ideas New app concept -t work,innovation
/add todo Fix bug #123 -p urgent -c development
```

## Notes

- **Lists are created automatically** - No need to create lists first, just add items!
- Items are assigned a globally unique auto-incrementing ID (#001, #002, ...)
- Default status is "pending"
- Default priority is "medium"

## Aliases

- `/a`

## Related Commands

- `/list` - Display items in list
- `/update` - Update item fields
- `/remove` - Remove item
- `/done` - Mark item as complete

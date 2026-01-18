# /update

Update one or more fields of an existing item.

## Usage

```
/update <id> [options]
```

## Arguments

- `id` (required) - The item ID to update

## Options

- `-d, --description <text>` - Update item description
- `-p, --priority <level>` - Update priority: urgent, high, medium, low
- `-S, --status <status>` - Update status: pending, active, in_progress, done
- `-c, --category <name>` - Update category

## Examples

```
/update 1 -d "Updated description"
/update 5 -p urgent
/update 10 -S in_progress
/update 3 -c work
/update 7 -p high -S active -c development
```

## Notes

- You can update multiple fields at once
- At least one option must be specified
- Use `/list` to see item IDs

## Aliases

- `/u`
- `/edit`

## Related Commands

- `/list` - Display items with IDs
- `/done` - Quick shortcut to mark as done
- `/add` - Add new item
- `/move` - Move item to different list

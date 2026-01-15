# /st

Show tasks with filtering and sorting options.

## Usage

```
/st                          # Show all open tasks
/st work                     # Filter by category
/st -p high                  # Filter by priority
/st -s priority -o asc       # Sort by priority ascending
/st --status=completed       # Show completed tasks
```

## Options

- `-s, --sort=<field>` - Sort by: created_at, priority, category, due_date, title
- `-o, --order=<asc|desc>` - Sort order (default: desc for created, asc for others)
- `-p, --priority=<level>` - Filter by priority: urgent, high, medium, low
- `-c, --category=<name>` - Filter by category
- `-S, --status=<status>` - Filter by status: active, in_progress, completed

## Examples

```
/st                          # All open tasks
/st work                     # Work category tasks
/st -p urgent                # Urgent priority tasks
/st -S completed             # Completed tasks
/st -s due_date -o asc       # Sort by due date
```

## Aliases

- `/show-tasks`
- `/tasks`

## Related Commands

- `/list` - Show lists and list items

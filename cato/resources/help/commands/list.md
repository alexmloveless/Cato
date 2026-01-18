# /list

Display items from one or all lists with filtering and sorting options.

## Usage

```
/list [name] [options]
```

## Arguments

- `name` (optional) - Name of specific list to display. If omitted, shows items from all lists.

## Options

- `-s, --sort <field>` - Sort by field: priority, status, category, created_at, id (default: priority)
- `-o, --order <dir>` - Sort order: asc, desc (default: asc)
- `-S, --status <status>` - Filter by status: pending, active, in_progress, done, all (default: pending, active, in_progress)
- `-p, --priority <level>` - Filter by priority: urgent, high, medium, low
- `-c, --category <name>` - Filter by category
- `-t, --tag <tag>` - Filter by tag

## Examples

```
/list                           # Show pending items from all lists (sorted by priority)
/list todo                      # Show pending items in todo list
/list -S all                    # Show all items including done
/list todo -S done              # Show completed items in todo list
/list -p urgent                 # Show only urgent items
/list -c work                   # Show items in work category
/list -s created_at -o desc     # Sort by newest first
/list todo -t important         # Show items tagged as important
```

## Item Display

Items are displayed in a table with:
- **ID** - Global auto-incrementing ID (#001, #002, ...)
- **S** - Status emoji (⚪ pending, 🔵 active, 🟡 in_progress, ✅ done)
- **Priority** - Priority level with emoji (🔥 URG, ⚡ HIGH, ● MED, ○ LOW)
- **Category** - Optional category grouping
- **Description** - Item content
- **Tags** - Associated tags

## Aliases

- `/l`
- `/ls`

## Related Commands

- `/lists` - Show overview of all lists with counts
- `/add` - Add item to list
- `/update` - Update item fields
- `/done` - Mark item as complete
- `/remove` - Remove item

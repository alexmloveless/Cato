# /lists

Show overview of all lists with item counts and statistics.

## Usage

```
/lists
```

## Description

Displays a table showing all lists with:
- **Name** - List name
- **Description** - List description (if set)
- **Total** - Total number of items
- **Pending** - Count of items not yet done (pending, active, in_progress)
- **Done** - Count of completed items

## Creating Lists

Lists are created automatically when you add your first item:

```
/add shopping Buy milk          # Creates "shopping" list automatically
/add todo Complete report       # Creates "todo" list automatically
```

No separate "create list" command is needed!

## Examples

```
/lists                          # Show all lists with counts
```

## Output Example

```
┌─────────────┬──────────────────┬───────┬─────────┬──────┐
│ Name        │ Description      │ Total │ Pending │ Done │
├─────────────┼──────────────────┼───────┼─────────┼──────┤
│ todo        │ My todo list     │    15 │      12 │    3 │
│ shopping    │ Shopping items   │     8 │       8 │    0 │
│ ideas       │ Project ideas    │    23 │      23 │    0 │
└─────────────┴──────────────────┴───────┴─────────┴──────┘
```

## Aliases

- `/ll`

## Related Commands

- `/list` - Display items in list
- `/add` - Add item to list
- `/delete-list` - Delete entire list

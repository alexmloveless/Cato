# List System Functional Specification

## Overview

The list system provides a unified way to manage any type of list (todo, shopping, to_watch, etc.) through a consistent command interface. All lists share the same data model and command structure, making the system simple and flexible.

## Design Principles

1. **Unified Model**: One data structure for all list types
2. **Named Lists**: Support multiple independent lists with user-defined names
3. **Human-Readable IDs**: Sequential numeric IDs for easy reference
4. **Flexible Organization**: Status, category, priority, and tags for filtering
5. **Extensible**: Design allows future field additions without breaking changes

## Data Model

### List Item

All items in all lists share this structure:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | integer | Auto | Auto-increment | Unique numeric ID across all lists (001, 002, ...) |
| list_name | string | Yes | - | Name of the parent list |
| description | string | Yes | - | Item content/description |
| status | enum | No | pending | Item status: `pending`, `active`, `in_progress`, `done` |
| priority | enum | No | medium | Priority level: `urgent`, `high`, `medium`, `low` |
| category | string | No | null | Optional category for grouping |
| tags | string[] | No | [] | Array of tags for flexible categorization |
| created_at | datetime | Auto | now() | Creation timestamp |
| updated_at | datetime | Auto | now() | Last update timestamp |
| metadata | json | No | {} | Extensible field for future additions |

### List Metadata

Each list has associated metadata:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Unique list name |
| description | string | No | Optional list description |
| created_at | datetime | Auto | Creation timestamp |
| updated_at | datetime | Auto | Last update timestamp |
| item_count | integer | Computed | Number of items in list |

### Status Flow

```
pending (default) → active → in_progress → done
   ↓                  ↓           ↓
   └──────────────────┴───────────┴──────→ done
```

- Items can transition to `done` from any status
- `done` items are hidden by default
- All other statuses are visible by default

### Priority Levels

Priority affects default sorting:
1. `urgent` (highest)
2. `high`
3. `medium` (default)
4. `low`

### Future Extensibility

The `metadata` field supports future additions without schema changes:
- Due dates (datetime)
- Assignee (string)
- Subtasks (json array)
- Custom fields per list type

## Commands

### Command Aliases

All commands support short aliases for faster typing:

| Full Command | Alias | Description |
|--------------|-------|-------------|
| /lists | /ll | Show lists overview |
| /list | /l | Display list items |
| /add | /a | Add item |
| /remove | /rm | Remove item |
| /update | /u | Update item |
| /move | /mv | Move item to different list |
| /newlist | /nl | Create list |
| /dellist | /dl | Delete list |
| /clear | - | Clear items from list (no alias) |

> **Note:** `/ll` is reserved for directory listing (`/file list` alias)

### Display Commands

#### `/lists` (alias: `/ll`)

Show overview of all lists with item counts. No item details, just summary.

**Usage:**
```
/lists
/ll
```

**Output:**
```
┌─────────────────────────────────────────────────────┐
│ Available Lists (3 lists)                           │
├──────────────────┬──────────┬──────────┬────────────┤
│ Name             │ Items    │ Pending  │ Done       │
├──────────────────┼──────────┼──────────┼────────────┤
│ todo             │ 12       │ 8        │ 4          │
│ shopping         │ 5        │ 5        │ 0          │
│ to_watch         │ 23       │ 20       │ 3          │
└──────────────────┴──────────┴──────────┴────────────┘
```

#### `/list [name] [options]` (alias: `/l`)

Display items in one specific list OR all items from all lists.

**Usage:**
```
/list todo                      # Show items in todo list
/list                           # Show items from ALL lists (each list separate table)
/l todo                         # Short alias
/l todo -s status               # Sort by status instead of priority
/l todo -c work                 # Filter by category
/l todo -S done                 # Show done items
/l -p urgent                    # Show urgent items across all lists
```

**Options:**
| Flag | Long Form | Values | Default | Description |
|------|-----------|--------|---------|-------------|
| -s | --sort | priority, status, category, created, id | priority | Sort field |
| -o | --order | asc, desc | asc (priority), desc (created) | Sort direction |
| -S | --status | pending, active, in_progress, done, all | pending,active,in_progress | Status filter |
| -p | --priority | urgent, high, medium, low | all | Priority filter |
| -c | --category | string | all | Category filter |
| -t | --tag | string | all | Tag filter (matches any) |

**Display (single list):**
```
┌────────────────────────────────────────────────────────────────────┐
│ List: todo (8 items) - sorted by priority ↑                        │
├─────┬──────┬──────────┬──────────┬─────────────────────┬──────────┤
│ ID  │ S    │ Priority │ Category │ Description         │ Tags     │
├─────┼──────┼──────────┼──────────┼─────────────────────┼──────────┤
│ 005 │ 🔵   │ 🔥 URG   │ work     │ Fix critical bug    │ bug,p1   │
│ 023 │ 🟡   │ ⚡ HIGH  │ personal │ Call dentist        │ health   │
│ 012 │ 🔵   │ ● MED    │ work     │ Review PR #42       │ code     │
│ 008 │ ⚪   │ ○ LOW    │ home     │ Clean garage        │          │
└─────┴──────┴──────────┴──────────┴─────────────────────┴──────────┘
```

**Display (all lists):**
```
┌────────────────────────────────────────────────────────────────────┐
│ todo (8 items) - sorted by priority ↑                              │
├─────┬──────┬──────────┬──────────┬─────────────────────┬──────────┤
│ ID  │ S    │ Priority │ Category │ Description         │ Tags     │
├─────┼──────┼──────────┼──────────┼─────────────────────┼──────────┤
│ 005 │ 🔵   │ 🔥 URG   │ work     │ Fix critical bug    │ bug,p1   │
│ 023 │ 🟡   │ ⚡ HIGH  │ personal │ Call dentist        │ health   │
└─────┴──────┴──────────┴──────────┴─────────────────────┴──────────┘

┌────────────────────────────────────────────────────────────────────┐
│ shopping (5 items) - sorted by priority ↑                          │
├─────┬──────┬──────────┬──────────┬─────────────────────┬──────────┤
│ ID  │ S    │ Priority │ Category │ Description         │ Tags     │
├─────┼──────┼──────────┼──────────┼─────────────────────┼──────────┤
│ 034 │ 🔵   │ ⚡ HIGH  │          │ Milk                │ groceries│
│ 035 │ 🔵   │ ● MED    │          │ Apples              │ groceries│
└─────┴──────┴──────────┴──────────┴─────────────────────┴──────────┘
```

**Status Symbols:**
- ⚪ `pending` - Not started
- 🔵 `active` - Active/ready to work on
- 🟡 `in_progress` - Currently working on
- ✅ `done` - Completed

**Priority Symbols:**
- 🔥 `urgent`
- ⚡ `high`
- ● `medium`
- ○ `low`

### Item Management Commands

#### `/add <list> <description> [options]` (alias: `/a`)

Add a new item to a list. Creates the list if it doesn't exist.

**Usage:**
```
/add todo Fix the login bug
/a todo Review PR -p high -c code
/a shopping Milk -p urgent -t groceries
/a todo Implement feature X -t sprint-5 -t backend
```

**Options:**
| Flag | Long Form | Values | Default |
|------|-----------|--------|---------|
| -p | --priority | urgent, high, medium, low | medium |
| -S | --status | pending, active, in_progress | pending |
| -c | --category | string | null |
| -t | --tag | string (repeatable) | [] |

**Output:**
```
✓ Added item #042 to todo: "Fix the login bug"
  Priority: medium, Status: pending
```

#### `/remove <id>` (alias: `/rm`)

Remove an item by its ID. Since IDs are globally unique, no list name needed.

**Usage:**
```
/remove 042
/rm 035
```

**Output:**
```
✓ Removed item #042 from todo: "Fix the login bug"
```

**Error Cases:**
```
✗ Item #999 not found
```

#### `/update <id> [options]` (alias: `/u`)

Update fields of an existing item. Since IDs are globally unique, no list name needed.

**Usage:**
```
/update 042 -S in_progress
/u 042 -p urgent
/u 042 -d "Fix critical login bug"
/u 042 -c work -t bug -t p1
/u 042 --add-tag=security
/u 042 --remove-tag=p1
```

**Options:**
| Flag | Long Form | Description |
|------|-----------|-------------|
| -d | --description | Update description text |
| -S | --status | Change status |
| -p | --priority | Change priority |
| -c | --category | Change category |
| -t | --tag | Replace all tags |
| -T | --add-tag | Add a tag (keeps existing) |
| -R | --remove-tag | Remove a tag |

**Output:**
```
✓ Updated item #042 in todo
  Status: pending → in_progress
  Priority: medium → urgent
```

### List Management Commands

#### `/newlist <name> [description]` (alias: `/nl`)

Create a new named list.

**Usage:**
```
/newlist todo
/nl shopping "Weekly grocery list"
/nl to_watch "Movies and shows to watch"
```

**Output:**
```
✓ Created list: todo
✓ Created list: shopping - "Weekly grocery list"
```

**Error Cases:**
```
✗ List "todo" already exists
```

#### `/dellist <name> [-f]` (alias: `/dl`)

Delete a list and all its items.

**Usage:**
```
/dellist old_todos              # Prompts for confirmation if items exist
/dl old_todos -f                # Skip confirmation with force flag
```

**Options:**
| Flag | Long Form | Description |
|------|-----------|-------------|
| -f | --force | Skip confirmation prompt |

**Output:**
```
⚠ Warning: List "old_todos" contains 5 items. Use -f to confirm deletion.
✓ Deleted list: old_todos (5 items removed)
```

### Bulk Operations

#### `/clear <list> [-S status] [-f]`

Clear items from a list.

**Usage:**
```
/clear todo -S done             # Remove all done items
/clear shopping                 # Remove all items (prompts confirmation)
/clear todo -S done -f          # Force without confirmation
```

**Options:**
| Flag | Long Form | Values | Description |
|------|-----------|--------|-------------|
| -S | --status | pending, active, in_progress, done | Only clear items with this status |
| -f | --force | - | Skip confirmation prompt |

**Output:**
```
✓ Removed 12 done items from todo
⚠ Warning: This will remove all 5 items from shopping. Use -f to confirm.
```

#### `/move <id> <target_list>` (alias: `/mv`)

Move an item to a different list. Since IDs are globally unique, just specify the ID and target.

**Usage:**
```
/move 042 backlog               # Move item 042 to backlog list
/mv 035 completed_tasks         # Move with short alias
```

**Output:**
```
✓ Moved item #042 from todo to backlog
```

## Filtering and Sorting

### Default Behavior

When displaying lists:
1. **Default sort**: priority (ascending: urgent → low)
2. **Default filter**: status in [pending, active, in_progress] (excludes done)
3. **Show all fields**: id, status, priority, category, description, tags

### Sort Order Precedence

When sorting by priority:
```
urgent (highest)
  ↓
high
  ↓
medium
  ↓
low (lowest)
```

When items have the same priority, secondary sort by created_at (newest first).

### Multiple Filters

Filters are combined with AND logic:
```
/list todo --priority=high --category=work --tag=bug
```
Shows items that are: high priority AND in work category AND tagged with bug.

### Tag Filtering

Tag filter matches ANY of the item's tags:
```
/list --tag=urgent
```
Shows all items that have "urgent" in their tags array.

## Display Formatting

### Truncation Rules

- **Description**: Max 40 characters in table view, "..." if truncated
- **Category**: Max 12 characters
- **Tags**: Show first 2 tags, "+N" if more exist

### Table Width

- Default: 80 characters (terminal standard)
- Responsive: Adjust column widths based on content when possible
- Wrap: Long descriptions can wrap in expanded view

### Color Coding (if terminal supports)

- Urgent priority: Red
- High priority: Yellow
- In progress status: Blue
- Done status: Green (when shown)

## Error Handling

### Validation Errors

```
✗ Invalid priority: "critical". Use: urgent, high, medium, low
✗ Invalid status: "finished". Use: pending, active, in_progress, done
✗ Description is required
✗ List name cannot be empty
```

### Not Found Errors

```
✗ List "xyz" not found. Use /ll to see available lists.
✗ Item #999 not found
```

### Constraint Errors

```
✗ Cannot delete list "todo": contains 8 items. Use -f or /clear first.
✗ List name "todo" already exists
✗ Cannot move item to non-existent list "backlog"
```

## Use Cases

### Use Case 1: Personal Todo List

```bash
# Create list
/nl todo "Personal tasks"

# Add items
/a todo "Call dentist" -p high -c health
/a todo "Review code" -p medium -c work
/a todo "Buy groceries" -p low -c errands

# View tasks by priority
/l todo

# Update task status (no list name needed - ID is global)
/u 001 -S done

# View only work items
/l todo -c work
```

### Use Case 2: Shopping List

```bash
# Create and populate
/nl shopping
/a shopping "Milk" -p urgent -t dairy
/a shopping "Apples" -t fruit -t organic
/a shopping "Bread" -t bakery

# Check off items as purchased (no list name needed)
/u 005 -S done
/u 006 -S done

# Clear purchased items
/clear shopping -S done
```

### Use Case 3: Content Tracking

```bash
# Create watch list
/nl to_watch "Movies and shows"

# Add content with ratings
/a to_watch "The Matrix" -p high -c movie -t sci-fi
/a to_watch "Breaking Bad" -p medium -c series -t drama

# View all movies
/l to_watch -c movie

# Mark as watched (no list name needed)
/u 012 -S done
```

### Use Case 4: Multi-List Overview

```bash
# View all lists summary
/ll

# View all urgent items across lists
/l -p urgent

# View all work-related items
/l -c work
```

## Implementation Notes

### ID Assignment

- IDs are sequential integers starting at 1
- IDs are unique across ALL lists (not per-list)
- IDs are never reused, even after deletion
- System maintains a global counter

### Performance Considerations

- Index on: list_name, status, priority, category
- Full-text search on: description, tags (future)
- Pagination for lists with >100 items (future)

### Data Persistence

- SQLite database for all list data
- Atomic operations for consistency
- Transaction support for bulk operations

### Backward Compatibility

The current system has separate Tasks and Lists implementations. The technical specification will address:
- Migration strategy from old schema to new unified schema
- Command aliasing for backward compatibility
- Data preservation during migration

## Future Enhancements

These features are not in scope for initial implementation but should be accommodated by the data model:

1. **Due Dates**: Add due_date field via metadata
2. **Recurring Items**: Recurrence rules via metadata
3. **Subtasks**: Nested task structure via metadata
4. **Attachments**: File references via metadata
5. **Sharing**: Multi-user access control
6. **Templates**: List templates with pre-filled items
7. **Search**: Full-text search across descriptions
8. **Archive**: Archive completed lists
9. **Export**: Export lists to JSON/CSV
10. **Import**: Import from other todo apps

## Examples

### Complete Workflow Example

```bash
# Setup
/nl sprint_5 "Sprint 5 tasks"

# Add tasks
/a sprint_5 "Implement login API" -p high -c backend -t api -t auth
/a sprint_5 "Add login form" -p high -c frontend -t ui -t auth
/a sprint_5 "Write tests" -p medium -c testing -t auth
/a sprint_5 "Update docs" -p low -c docs -t auth

# View tasks by priority
/l sprint_5
# Output shows: 2 high, 1 medium, 1 low

# Start working (no list name needed - ID is global)
/u 001 -S in_progress

# Mark complete
/u 001 -S done

# View remaining work
/l sprint_5
# Output shows: 3 items (excludes done)

# View all including done
/l sprint_5 -S all

# Filter by tag
/l sprint_5 -t auth
# Output shows: all 4 items

# Clean up after sprint
/clear sprint_5 -S done
/dl sprint_5 -f
```

## Summary

This unified list system provides:

- **Simple**: One data model, consistent commands
- **Flexible**: Multiple named lists, rich metadata
- **Powerful**: Filtering, sorting, tagging, categories
- **Extensible**: Metadata field allows future enhancements
- **User-Friendly**: Human-readable IDs, clear output formatting

The system replaces the separate Tasks and Lists implementations with a single, more capable system that can handle any list-based workflow.

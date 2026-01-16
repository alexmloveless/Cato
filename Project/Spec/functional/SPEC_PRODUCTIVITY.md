# Productivity System Specification

> **⚠️ DEPRECATED:** This specification describes the old separate Tasks and Lists system.
>
> **See [SPEC_LISTS.md](SPEC_LISTS.md) for the new unified list system.**
>
> The new system combines Tasks and Lists into a single unified model with:
> - One data structure for all list types
> - Globally unique numeric IDs
> - Short command aliases (/a, /l, /ls, /u, /rm, etc.)
> - Single-letter flags (-p, -s, -c, -t, -S)
> - No list name needed for updates/removes (global IDs)

## Overview (OLD SYSTEM)

The productivity system provides task management and list organization through explicit slash commands. It uses a dedicated agent/service to manage productivity data stored in SQLite.


## Entity Types

### Tasks

Tasks represent actionable items with optional due dates, categories, and priorities.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Task title |
| description | string | No | Task details |
| status | enum | No | active, in_progress, completed, deleted |
| due_date | datetime | No | When task is due |
| category | string | No | Project or category name |
| priority | enum | No | urgent, high, medium, low |
| pseudo_id | string | Auto | Human-readable ID (task001, task002) |
| created_at | datetime | Auto | Creation timestamp |
| updated_at | datetime | Auto | Last update timestamp |


**Status Transitions:**
- `active` → `in_progress` → `completed`
- `active` → `deleted`
- Any status → `deleted`

### Lists and List Items

Lists provide a way to organize items into named collections (shopping, projects, ideas, etc.).

**List Item Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Item description |
| list_id | string | Yes | ID of the parent list |
| checked | bool | No | Item completed flag |
| position | int | No | Sort/order position |
| pseudo_id | string | Auto | Human-readable ID (001) |
| created_at | datetime | Auto | Creation timestamp |


## Commands

### /st (Show Tasks)

Display open tasks with filtering and sorting options.

**Usage:**
```
/st                              # All open tasks
/st work                         # Filter by category
/st -p high                      # Filter by priority
/st -s priority -o asc           # Sort by priority ascending
/st --status=completed           # Show completed tasks
```

**Options:**
| Option | Values | Default |
|--------|--------|---------|
| -s, --sort | created, priority, category, due, id, status | created |
| -o, --order | asc, desc | desc (for created), asc (others) |
| -p, --priority | urgent, high, medium, low | none |
| -c, --category | any string | none |
| -S, --status | active, in_progress, completed | active + in_progress |

**Display:**
```
┌──────────────────────────────────────────────────────────┐
│ Open Tasks sorted by created ↓ (5)                       │
├─────┬──────────┬──────────┬───────┬─────────────┬────────┤
│ S   │ Priority │ Category │ ID    │ Task        │ Due    │
├─────┼──────────┼──────────┼───────┼─────────────┼────────┤
│ 🔵  │ 🔥 URGENT│ work     │ 005   │ Fix bug     │ Today  │
│ 🟡  │ ⚡ HIGH  │ personal │ 004   │ Call dentist│ 01/15  │
│ 🔵  │ ● MED    │ work     │ 003   │ Review doc  │        │
└─────┴──────────┴──────────┴───────┴─────────────┴────────┘
```

### /list (Show Lists)

Display lists and list items.

**Usage:**
```
/list                    # Show all lists with item counts
/list shopping           # Show items in shopping list
```

**List Overview Display:**
```
┌─────────────────────────────────────┐
│ Available Lists (3 lists)           │
├─────────────────┬───────────────────┤
│ List Name       │ Items             │
├─────────────────┼───────────────────┤
│ shopping        │ 12                │
│ ideas           │ 5                 │
│ books           │ 8                 │
└─────────────────┴───────────────────┘
```

**List Items Display:**
```
┌───────────────────────────────────────────────┐
│ List: shopping (12 items)                     │
├───────┬─────┬────────────────────┬───────────┤
│ ID    │ S   │ Item               │ Added     │
├───────┼─────┼────────────────────┼───────────┤
│ 001   │ 🔵  │ Milk               │ 01/10     │
│ 002   │ 🔵  │ Apples             │ 01/10     │
│ 003   │ ✅  │ Bread              │ 01/09     │
└───────┴─────┴────────────────────┴───────────┘
```


## Storage

### SQLite Database
Productivity data is stored in SQLite for:
- Persistence across sessions
- Efficient querying and filtering
- Structured data with relationships

### Pseudo IDs
All entities receive human-readable IDs:
- Tasks: `001`, `002`, ...
- List items: `001`, `002`, ...

IDs are assigned sequentially and used for:
- Display in tables
- Reference in commands
- Updates and deletions

## Integration with Chat

### Productivity Agent
A dedicated AI agent processes productivity requests:
- Determines appropriate action
- Executes database operations
- Returns formatted response

### Response Format
Productivity responses are displayed in the assistant panel but not added to conversation history, keeping the main LLM context clean.

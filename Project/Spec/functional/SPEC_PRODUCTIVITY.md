# Productivity System Specification

## Overview

The productivity system provides task management, list organization, time tracking, and memory storage through natural language interaction. It uses a dedicated AI agent to parse requests and manage productivity data stored in SQLite.

## Routing

### Marker-Based Routing
Messages prefixed with `%` (configurable via `productivity.routing_marker`) are routed to the productivity agent.

Examples:
```
% create a task to review the report due Friday
% add milk to my shopping list
% log 4 hours on project alpha today
```

### Natural Language Processing
The productivity agent interprets natural language to:
- Identify the action (create, update, delete, show)
- Extract entity details (title, due date, category, priority)
- Parse dates and times in various formats
- Handle ambiguous requests with reasonable defaults

## Entity Types

### Tasks

Tasks represent actionable items with optional due dates, categories, and priorities.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Task description |
| status | enum | No | active, in_progress, completed, deleted |
| due_date | datetime | No | When task is due |
| category | string | No | Project or category name |
| priority | enum | No | urgent, high, medium, low |
| tags | list | No | Additional tags |
| pseudo_id | string | Auto | Human-readable ID (task001, task002) |
| created_at | datetime | Auto | Creation timestamp |
| updated_at | datetime | Auto | Last update timestamp |

**Natural Language Examples:**
```
% create a task to review the quarterly report
% add a high priority task: fix the login bug for the auth project
% create task: call the dentist, due tomorrow
% urgent task: submit tax return by April 15th, category: finance
```

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
| list_name | string | Yes | Name of the list |
| status | enum | No | active, completed, archived |
| category | string | No | Sub-category within list |
| pseudo_id | string | Auto | Human-readable ID (item001) |
| created_at | datetime | Auto | Creation timestamp |

**Natural Language Examples:**
```
% add milk to my shopping list
% add eggs, bread, and butter to shopping
% add "new project idea" to my ideas list
% add item: review competitor sites, list: research, category: marketing
```

### Timelog Entries

Time tracking for projects with flexible date and duration input.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| project | string | Yes | Project name |
| hours | float | Yes | Hours worked |
| date | date | Yes | Date of work |
| note | string | No | Additional notes |
| pseudo_id | string | Auto | Human-readable ID (timelog001) |
| created_at | datetime | Auto | Creation timestamp |

**Duration Shortcuts:**
| Input | Hours |
|-------|-------|
| "half day" | 4.0 |
| "full day" | 8.0 |
| "all day" | 8.0 |
| "2 hours" | 2.0 |
| "1.5 hours" | 1.5 |
| "30 minutes" | 0.5 |

**Date Shortcuts:**
- `today`, `yesterday`
- `Monday`, `Tuesday`, etc. (most recent)
- `last Monday`, `next Friday`
- `6th June`, `June 6th`, `2024-06-06`

**Natural Language Examples:**
```
% I worked half day today on project nx with a note that I presented to the board
% log a half day against project alpha for yesterday
% worked all day on project beta on 6th June 25
% log 3 hours on database optimization today
```

### Memories

Memories store personal facts, preferences, and important information for future reference.

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | The memory content |
| category | string | No | Memory category |
| pseudo_id | string | Auto | Human-readable ID (memory001) |
| created_at | datetime | Auto | Creation timestamp |

**Natural Language Examples:**
```
% remember that my favorite color is blue
% remember I have a meeting with John every Tuesday
% remember my API key expires on Dec 31st
```

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
┌─────────────────────────────────────────────────────────────┐
│ Open Tasks sorted by created ↓ (5)                          │
├─────┬──────────┬──────────┬─────────┬─────────────┬────────┤
│ S   │ Priority │ Category │ ID      │ Task        │ Due    │
├─────┼──────────┼──────────┼─────────┼─────────────┼────────┤
│ 🔵  │ 🔥 URGENT│ work     │ task005 │ Fix bug     │ Today  │
│ 🟡  │ ⚡ HIGH  │ personal │ task004 │ Call dentist│ 01/15  │
│ 🔵  │ ● MED    │ work     │ task003 │ Review doc  │        │
└─────┴──────────┴──────────┴─────────┴─────────────┴────────┘
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
┌─────────────────────────────────────────────────────────────┐
│ List: shopping (12 items)                                   │
├───────────┬─────┬──────────┬────────────────────┬───────────┤
│ ID        │ S   │ Category │ Item               │ Added     │
├───────────┼─────┼──────────┼────────────────────┼───────────┤
│ item001   │ 🔵  │ dairy    │ Milk               │ 01/10     │
│ item002   │ 🔵  │ produce  │ Apples             │ 01/10     │
│ item003   │ ✅  │ bakery   │ Bread              │ 01/09     │
└───────────┴─────┴──────────┴────────────────────┴───────────┘
```

### /timelog (Show Timelog)

Display and export timelog entries.

**Usage:**
```
/timelog                              # Show all entries
/tl -p project_name                   # Filter by project
/tl --start=2024-01-01                # Filter from date
/tl --end=2024-12-31                  # Filter to date
/tl -g project                        # Group by project
/tl -g week                           # Group by week
/tl -g month                          # Group by month
/tl -o csv -f output.csv              # Export to CSV
/tl --output=json --file=data.json    # Export to JSON
/tl -o yaml -f output.yaml            # Export to YAML
```

**Options:**
| Option | Values | Default |
|--------|--------|---------|
| -p, --project | any string | none (all projects) |
| -s, --start | date | none |
| -e, --end | date | none |
| -g, --group | project, week, month | none |
| -o, --output | csv, json, yaml | none (display only) |
| -f, --file | filepath | required if -o specified |

**Display (Ungrouped):**
```
┌─────────────────────────────────────────────────────────────┐
│ Timelog Entries (25 entries, 87.5 hours)                    │
├───────────┬────────────┬───────┬────────────────────────────┤
│ ID        │ Date       │ Hours │ Project       │ Note       │
├───────────┼────────────┼───────┼───────────────┼────────────┤
│ timelog025│ 2024-01-15 │ 8.0   │ project-alpha │ Board mtg  │
│ timelog024│ 2024-01-14 │ 4.0   │ project-beta  │            │
└───────────┴────────────┴───────┴───────────────┴────────────┘
```

**Display (Grouped by Project):**
```
┌─────────────────────────────────────────────────────────────┐
│ Timelog by Project (87.5 hours total)                       │
├─────────────────┬───────────────────────────────────────────┤
│ Project         │ Hours                                     │
├─────────────────┼───────────────────────────────────────────┤
│ project-alpha   │ 52.0                                      │
│ project-beta    │ 35.5                                      │
└─────────────────┴───────────────────────────────────────────┘
```

## Proactive Memory Suggestions

When enabled (`productivity.proactive_memory_suggestions: true`), the system detects personal facts in user messages and offers to store them.

**Trigger Examples:**
- "My name is Alex"
- "I prefer dark mode"
- "My birthday is June 15th"

**User Flow:**
```
User: My favorite programming language is Python

🧠  It looks like you just shared something important:

    "My favorite programming language is Python"

Would you like me to remember this for you? (yes/no)
```

User responds `yes` → Memory stored with automatic ID
User responds `no` → Continue without storing

## Storage

### SQLite Database
Productivity data is stored in SQLite for:
- Persistence across sessions
- Efficient querying and filtering
- Structured data with relationships

### Pseudo IDs
All entities receive human-readable IDs:
- Tasks: `task001`, `task002`, ...
- List items: `item001`, `item002`, ...
- Timelog entries: `timelog001`, `timelog002`, ...
- Memories: `memory001`, `memory002`, ...

IDs are assigned sequentially and used for:
- Display in tables
- Reference in commands
- Updates and deletions

## Integration with Chat

### Productivity Agent
A dedicated AI agent (using pydantic-ai) processes productivity requests:
- Parses natural language input
- Determines appropriate action
- Executes database operations
- Returns formatted response

### Response Format
Productivity responses are displayed in the assistant panel but not added to conversation history, keeping the main LLM context clean.

### Vector Store Integration
Productivity exchanges are stored in the vector store for:
- Future context retrieval
- Thread continuation support

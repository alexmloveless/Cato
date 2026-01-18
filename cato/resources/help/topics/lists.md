# List Management System

Cato provides a unified list management system for organizing items across multiple lists with powerful filtering, sorting, and status tracking.

## Overview

The list system uses:
- **Global IDs**: Auto-incrementing IDs across all lists (#001, #002, #003...)
- **Named Lists**: Organize items into named collections (todo, shopping, ideas, etc.)
- **Status Tracking**: Four status levels (pending, active, in_progress, done)
- **Priority Levels**: Four priority levels (urgent, high, medium, low)
- **Categories**: Optional grouping within lists
- **Tags**: Multiple tags per item for flexible organization

## Quick Start

### Create Your First Item

**Note:** Lists are created automatically - just add an item!

```
/add todo Complete project report
```

This automatically:
- Creates a new list named "todo" (if it doesn't exist)
- Adds an item with ID #001 and status "pending"

No separate "create list" command is needed!

### View Items
```
/list                           # See all pending items
/list todo                      # See pending items in todo list
/list -S all                    # See all items including completed
```

### Complete an Item
```
/done 1                         # Mark item #001 as complete
```

### Update an Item
```
/update 1 -p high               # Set priority to high
/update 1 -S in_progress        # Mark as in progress
/update 1 -c work               # Set category to "work"
```

## Common Workflows

### Shopping List
```
/add shopping Milk -c dairy
/add shopping Bread -c bakery
/add shopping Apples -c produce
/list shopping                  # View shopping items
/done 1                         # Mark as bought
```

### Project Management
```
/add project Design UI -p high -t design,frontend
/add project Write tests -p medium -t testing
/add project Deploy -p urgent -t devops
/list project -p urgent         # See urgent tasks
/update 1 -S in_progress        # Mark as started
/done 1                         # Mark as complete
```

### Idea Collection
```
/add ideas New app concept -t innovation
/add ideas Blog post topic -t writing
/list ideas                     # Review all ideas
/move 5 project                 # Convert idea to project
```

## Status Workflow

Items typically follow this status progression:

1. **pending** (⚪) - Not started
2. **active** (🔵) - Ready to work on
3. **in_progress** (🟡) - Currently working
4. **done** (✅) - Completed

Default behavior:
- New items start as "pending"
- `/list` shows pending, active, and in_progress by default
- Use `/list -S done` to see completed items

## Priority Levels

- **🔥 urgent** - Critical, immediate attention
- **⚡ high** - Important, prioritize soon
- **● medium** - Normal priority (default)
- **○ low** - Can wait

Items are sorted by priority by default (urgent first).

## Filtering and Sorting

### Filter by Status
```
/list -S pending                # Only pending items
/list -S done                   # Only completed items
/list -S all                    # All items
```

### Filter by Priority
```
/list -p urgent                 # Only urgent items
/list -p high                   # Only high priority
```

### Filter by Category
```
/list -c work                   # Only work items
/list todo -c personal          # Personal items in todo list
```

### Filter by Tag
```
/list -t important              # Items tagged as important
```

### Sort Options
```
/list -s created_at -o desc     # Newest first
/list -s priority -o asc        # Urgent first (default)
/list -s category               # Group by category
```

## List Management

### View All Lists
```
/lists                          # Overview with counts
```

### Move Items Between Lists
```
/move 5 shopping                # Move item #005 to shopping list
```

### Clear Completed Items
```
/lclear todo -S done            # Remove done items from todo
```

### Delete a List
```
/delete-list old_project -f     # Delete list and all items
```

## Tips

1. **Auto-creation**: Lists are created automatically when you add the first item
2. **Global IDs**: Item IDs are unique across all lists, making them easy to reference
3. **Default filters**: `/list` shows only pending/active/in_progress items by default
4. **Quick completion**: Use `/done <id>` instead of `/update <id> -S done`
5. **Batch operations**: Use `/lclear` with status filters to clean up multiple items

## Available Commands

- `/lists` - Show all lists overview
- `/list [name]` - Display items with filtering
- `/add <list> <description>` - Add new item
- `/update <id>` - Update item fields
- `/done <id>` - Mark as complete
- `/move <id> <list>` - Move between lists
- `/remove <id>` - Delete item
- `/lclear <list>` - Clear items from list
- `/delete-list <name>` - Delete entire list

For detailed help on any command, use `/help <command>`.

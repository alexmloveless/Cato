# List System Technical Specification

## Overview

This document defines the technical implementation of Cato's unified list system. The system provides a single data model and command interface for all types of lists (todo, shopping, to_watch, etc.).

See [SPEC_LISTS.md](../functional/SPEC_LISTS.md) for the functional specification.

## Design Principles

1. **Single Table**: One table for all list items across all lists
2. **Global IDs**: Sequential integer IDs unique across all lists
3. **Simple Schema**: Minimal schema with extensibility via metadata field
4. **No Backward Compatibility**: Clean slate implementation, databases will be purged

## Database Schema

### Lists Table

Stores metadata about each named list.

```sql
CREATE TABLE IF NOT EXISTS lists (
    name TEXT PRIMARY KEY,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT
);

CREATE INDEX IF NOT EXISTS idx_lists_created ON lists(created_at);
```

**Fields:**
- `name`: Unique list name (e.g., "todo", "shopping")
- `description`: Optional description
- `created_at`: ISO 8601 timestamp
- `updated_at`: ISO 8601 timestamp
- `metadata`: JSON for future extensibility

### List Items Table

Stores all items for all lists.

```sql
CREATE TABLE IF NOT EXISTS list_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_name TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    priority TEXT NOT NULL DEFAULT 'medium',
    category TEXT,
    tags TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (list_name) REFERENCES lists(name) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_list_items_list_name ON list_items(list_name);
CREATE INDEX IF NOT EXISTS idx_list_items_status ON list_items(status);
CREATE INDEX IF NOT EXISTS idx_list_items_priority ON list_items(priority);
CREATE INDEX IF NOT EXISTS idx_list_items_category ON list_items(category);
CREATE INDEX IF NOT EXISTS idx_list_items_created ON list_items(created_at);
```

**Fields:**
- `id`: Auto-incrementing integer (001, 002, ...), globally unique
- `list_name`: FK to lists table
- `description`: Item content
- `status`: Enum (pending, active, in_progress, done)
- `priority`: Enum (urgent, high, medium, low)
- `category`: Optional grouping category
- `tags`: JSON array of tag strings
- `created_at`: ISO 8601 timestamp
- `updated_at`: ISO 8601 timestamp
- `metadata`: JSON for future extensibility (due dates, etc.)

**Indexes:**
- list_name: Fast filtering by list
- status: Fast filtering by status
- priority: Fast sorting by priority
- category: Fast filtering by category
- created_at: Secondary sort key

### Schema Notes

1. **Foreign Key Cascade**: Deleting a list automatically removes all its items
2. **Tag Storage**: Tags stored as JSON array `["tag1", "tag2"]`
3. **Priority Order**: Map to integers for sorting (urgent=1, high=2, medium=3, low=4)
4. **Status Values**: Validated at application layer, not DB constraint
5. **Metadata Field**: Allows future additions without schema changes

## Data Models

### List Entity

```python
from pydantic import BaseModel, Field

class List(BaseModel):
    """
    Named list metadata.

    Attributes
    ----------
    name : str
        Unique list name.
    description : str | None
        Optional description.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    metadata : dict
        Extensible metadata.
    """
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    metadata: dict = Field(default_factory=dict)
```

### ListItem Entity

```python
from typing import Literal

class ListItem(BaseModel):
    """
    Item in a list.

    Attributes
    ----------
    id : int
        Globally unique auto-incrementing ID.
    list_name : str
        Name of parent list.
    description : str
        Item content.
    status : Literal
        Item status (pending, active, in_progress, done).
    priority : Literal
        Priority level (urgent, high, medium, low).
    category : str | None
        Optional category.
    tags : list[str]
        List of tags.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    metadata : dict
        Extensible metadata.
    """
    id: int | None = None  # None for new items
    list_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1, max_length=500)
    status: Literal["pending", "active", "in_progress", "done"] = "pending"
    priority: Literal["urgent", "high", "medium", "low"] = "medium"
    category: str | None = Field(None, max_length=50)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)

    @property
    def display_id(self) -> str:
        """Format ID as zero-padded 3-digit string."""
        return f"{self.id:03d}" if self.id else "???"

    @property
    def priority_order(self) -> int:
        """Return integer for priority sorting (1=urgent, 4=low)."""
        priority_map = {"urgent": 1, "high": 2, "medium": 3, "low": 4}
        return priority_map[self.priority]
```

## Data Access Layer

### ListRepository

```python
import json
from datetime import datetime
from typing import Literal

class ListRepository:
    """Repository for list operations."""

    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_list(self, name: str) -> List | None:
        """
        Get list by name.

        Parameters
        ----------
        name : str
            List name.

        Returns
        -------
        List | None
            List if found, None otherwise.
        """
        row = await self._db.fetchone(
            "SELECT * FROM lists WHERE name = ?",
            (name,)
        )
        return self._row_to_list(row) if row else None

    async def get_all_lists(self) -> list[List]:
        """Get all lists ordered by name."""
        rows = await self._db.fetchall(
            "SELECT * FROM lists ORDER BY name ASC"
        )
        return [self._row_to_list(row) for row in rows]

    async def create_list(self, lst: List) -> str:
        """
        Create new list.

        Parameters
        ----------
        lst : List
            List to create.

        Returns
        -------
        str
            List name.
        """
        now = datetime.now().isoformat()
        await self._db.execute(
            """
            INSERT INTO lists (name, description, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                lst.name,
                lst.description,
                now,
                now,
                json.dumps(lst.metadata) if lst.metadata else None,
            )
        )
        return lst.name

    async def delete_list(self, name: str) -> None:
        """Delete list by name (cascades to items)."""
        await self._db.execute("DELETE FROM lists WHERE name = ?", (name,))

    async def count_items(self, list_name: str) -> int:
        """Count items in a list."""
        row = await self._db.fetchone(
            "SELECT COUNT(*) as count FROM list_items WHERE list_name = ?",
            (list_name,)
        )
        return row["count"] if row else 0

    async def count_items_by_status(
        self, list_name: str, status: str
    ) -> int:
        """Count items with specific status in a list."""
        row = await self._db.fetchone(
            """
            SELECT COUNT(*) as count FROM list_items
            WHERE list_name = ? AND status = ?
            """,
            (list_name, status)
        )
        return row["count"] if row else 0

    def _row_to_list(self, row: dict) -> List:
        """Convert DB row to List entity."""
        return List(
            name=row["name"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
```

### ListItemRepository

```python
class ListItemRepository:
    """Repository for list item operations."""

    def __init__(self, db: Database) -> None:
        self._db = db

    async def get(self, id: int) -> ListItem | None:
        """
        Get item by ID.

        Parameters
        ----------
        id : int
            Item ID.

        Returns
        -------
        ListItem | None
            Item if found.
        """
        row = await self._db.fetchone(
            "SELECT * FROM list_items WHERE id = ?",
            (id,)
        )
        return self._row_to_item(row) if row else None

    async def get_all(
        self,
        list_name: str | None = None,
        status: list[str] | None = None,
        priority: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        sort_by: str = "priority",
        order: str = "asc",
    ) -> list[ListItem]:
        """
        Get items with optional filters.

        Parameters
        ----------
        list_name : str | None
            Filter by list name.
        status : list[str] | None
            Filter by status values.
        priority : str | None
            Filter by priority.
        category : str | None
            Filter by category.
        tag : str | None
            Filter by tag (matches any).
        sort_by : str
            Sort field (priority, status, category, created, id).
        order : str
            Sort order (asc, desc).

        Returns
        -------
        list[ListItem]
            Matching items.
        """
        query = "SELECT * FROM list_items WHERE 1=1"
        params = []

        if list_name:
            query += " AND list_name = ?"
            params.append(list_name)

        if status:
            placeholders = ",".join("?" * len(status))
            query += f" AND status IN ({placeholders})"
            params.extend(status)

        if priority:
            query += " AND priority = ?"
            params.append(priority)

        if category:
            query += " AND category = ?"
            params.append(category)

        if tag:
            # Tags stored as JSON array, use JSON functions
            query += " AND json_each.value = ?"
            query = query.replace(
                "WHERE 1=1",
                "FROM list_items, json_each(list_items.tags) WHERE 1=1"
            )
            params.append(tag)

        # Validate sort field
        valid_sorts = {"priority", "status", "category", "created_at", "id"}
        if sort_by not in valid_sorts:
            sort_by = "priority"

        # Map sort field to column
        sort_column = sort_by
        if sort_by == "priority":
            # Sort by priority order (urgent=1, low=4)
            sort_column = """
            CASE priority
                WHEN 'urgent' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
            END
            """

        order_dir = "DESC" if order.lower() == "desc" else "ASC"
        query += f" ORDER BY {sort_column} {order_dir}, created_at DESC"

        rows = await self._db.fetchall(query, tuple(params))
        return [self._row_to_item(row) for row in rows]

    async def create(self, item: ListItem) -> int:
        """
        Create new item.

        Parameters
        ----------
        item : ListItem
            Item to create.

        Returns
        -------
        int
            New item ID.
        """
        now = datetime.now().isoformat()
        cursor = await self._db.execute(
            """
            INSERT INTO list_items (
                list_name, description, status, priority, category,
                tags, created_at, updated_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.list_name,
                item.description,
                item.status,
                item.priority,
                item.category,
                json.dumps(item.tags) if item.tags else "[]",
                now,
                now,
                json.dumps(item.metadata) if item.metadata else None,
            )
        )
        return cursor.lastrowid

    async def update(self, item: ListItem) -> None:
        """
        Update existing item.

        Parameters
        ----------
        item : ListItem
            Item to update (must have id).
        """
        if not item.id:
            raise ValueError("Cannot update item without ID")

        item.updated_at = datetime.now()
        await self._db.execute(
            """
            UPDATE list_items SET
                list_name = ?, description = ?, status = ?, priority = ?,
                category = ?, tags = ?, updated_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                item.list_name,
                item.description,
                item.status,
                item.priority,
                item.category,
                json.dumps(item.tags) if item.tags else "[]",
                item.updated_at.isoformat(),
                json.dumps(item.metadata) if item.metadata else None,
                item.id,
            )
        )

    async def delete(self, id: int) -> None:
        """Delete item by ID."""
        await self._db.execute("DELETE FROM list_items WHERE id = ?", (id,))

    async def delete_by_status(
        self, list_name: str, status: str
    ) -> int:
        """
        Delete items by list and status.

        Returns
        -------
        int
            Number of items deleted.
        """
        result = await self._db.execute(
            "DELETE FROM list_items WHERE list_name = ? AND status = ?",
            (list_name, status)
        )
        return result.rowcount

    def _row_to_item(self, row: dict) -> ListItem:
        """Convert DB row to ListItem entity."""
        return ListItem(
            id=row["id"],
            list_name=row["list_name"],
            description=row["description"],
            status=row["status"],
            priority=row["priority"],
            category=row["category"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
```

## Service Layer

### ListService

```python
class ListService:
    """Service for list operations (business logic)."""

    def __init__(
        self,
        list_repo: ListRepository,
        item_repo: ListItemRepository,
    ) -> None:
        self._lists = list_repo
        self._items = item_repo

    async def create_list(
        self, name: str, description: str | None = None
    ) -> List:
        """
        Create new list.

        Parameters
        ----------
        name : str
            List name (must be unique).
        description : str | None
            Optional description.

        Returns
        -------
        List
            Created list.

        Raises
        ------
        ValueError
            If list name already exists.
        """
        # Check if exists
        existing = await self._lists.get_list(name)
        if existing:
            raise ValueError(f"List '{name}' already exists")

        lst = List(
            name=name,
            description=description,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        await self._lists.create_list(lst)
        return lst

    async def get_list_overview(self) -> list[dict]:
        """
        Get overview of all lists with item counts.

        Returns
        -------
        list[dict]
            List of dicts with keys: name, description, total, pending, done.
        """
        lists = await self._lists.get_all_lists()
        overview = []

        for lst in lists:
            total = await self._lists.count_items(lst.name)
            pending = await self._lists.count_items_by_status(
                lst.name, "pending"
            ) + await self._lists.count_items_by_status(
                lst.name, "active"
            ) + await self._lists.count_items_by_status(
                lst.name, "in_progress"
            )
            done = await self._lists.count_items_by_status(lst.name, "done")

            overview.append({
                "name": lst.name,
                "description": lst.description,
                "total": total,
                "pending": pending,
                "done": done,
            })

        return overview

    async def delete_list(
        self, name: str, force: bool = False
    ) -> tuple[bool, str]:
        """
        Delete list and all items.

        Parameters
        ----------
        name : str
            List name.
        force : bool
            Skip confirmation check.

        Returns
        -------
        tuple[bool, str]
            (success, message).
        """
        lst = await self._lists.get_list(name)
        if not lst:
            return False, f"List '{name}' not found"

        item_count = await self._lists.count_items(name)

        if not force and item_count > 0:
            return (
                False,
                f"List '{name}' contains {item_count} items. Use -f to confirm."
            )

        await self._lists.delete_list(name)
        return True, f"Deleted list: {name} ({item_count} items removed)"

    async def add_item(
        self,
        list_name: str,
        description: str,
        priority: str = "medium",
        status: str = "pending",
        category: str | None = None,
        tags: list[str] | None = None,
    ) -> ListItem:
        """
        Add item to list (creates list if doesn't exist).

        Parameters
        ----------
        list_name : str
            Target list name.
        description : str
            Item description.
        priority : str
            Priority level.
        status : str
            Initial status.
        category : str | None
            Optional category.
        tags : list[str] | None
            Optional tags.

        Returns
        -------
        ListItem
            Created item.
        """
        # Create list if doesn't exist
        existing = await self._lists.get_list(list_name)
        if not existing:
            await self.create_list(list_name)

        item = ListItem(
            list_name=list_name,
            description=description,
            status=status,
            priority=priority,
            category=category,
            tags=tags or [],
        )

        item_id = await self._items.create(item)
        item.id = item_id
        return item

    async def update_item(
        self,
        id: int,
        **updates,
    ) -> tuple[bool, str, ListItem | None]:
        """
        Update item fields.

        Parameters
        ----------
        id : int
            Item ID.
        **updates
            Fields to update (description, status, priority, etc.).

        Returns
        -------
        tuple[bool, str, ListItem | None]
            (success, message, updated item).
        """
        item = await self._items.get(id)
        if not item:
            return False, f"Item #{id:03d} not found", None

        # Apply updates
        for key, value in updates.items():
            if value is not None and hasattr(item, key):
                setattr(item, key, value)

        await self._items.update(item)
        return True, f"Updated item #{item.display_id}", item

    async def remove_item(self, id: int) -> tuple[bool, str]:
        """
        Remove item by ID.

        Parameters
        ----------
        id : int
            Item ID.

        Returns
        -------
        tuple[bool, str]
            (success, message).
        """
        item = await self._items.get(id)
        if not item:
            return False, f"Item #{id:03d} not found"

        await self._items.delete(id)
        return (
            True,
            f"Removed item #{item.display_id} from {item.list_name}: \"{item.description}\""
        )

    async def move_item(
        self, id: int, target_list: str
    ) -> tuple[bool, str]:
        """
        Move item to different list.

        Parameters
        ----------
        id : int
            Item ID.
        target_list : str
            Target list name.

        Returns
        -------
        tuple[bool, str]
            (success, message).
        """
        item = await self._items.get(id)
        if not item:
            return False, f"Item #{id:03d} not found"

        # Create target list if doesn't exist
        existing = await self._lists.get_list(target_list)
        if not existing:
            await self.create_list(target_list)

        old_list = item.list_name
        item.list_name = target_list
        await self._items.update(item)

        return (
            True,
            f"Moved item #{item.display_id} from {old_list} to {target_list}"
        )

    async def clear_items(
        self, list_name: str, status: str | None = None, force: bool = False
    ) -> tuple[bool, str]:
        """
        Clear items from list.

        Parameters
        ----------
        list_name : str
            List name.
        status : str | None
            Only clear items with this status.
        force : bool
            Skip confirmation.

        Returns
        -------
        tuple[bool, str]
            (success, message).
        """
        lst = await self._lists.get_list(list_name)
        if not lst:
            return False, f"List '{list_name}' not found"

        if status:
            # Delete by status
            count = await self._items.delete_by_status(list_name, status)
            return True, f"Removed {count} {status} items from {list_name}"
        else:
            # Delete all items
            count = await self._lists.count_items(list_name)
            if not force and count > 0:
                return (
                    False,
                    f"This will remove all {count} items from {list_name}. Use -f to confirm."
                )

            await self._lists.delete_list(list_name)
            await self.create_list(list_name, lst.description)
            return True, f"Cleared all {count} items from {list_name}"
```

## Command Layer

Commands are implemented in `cato/commands/lists.py` using the `@command` decorator.

### Command Structure

```python
from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command

@command(
    name="list",
    description="Display items in list(s)",
    usage="/list [name] [-s sort] [-o order] [-S status] [-p priority] [-c category] [-t tag]",
    aliases=["l"],
)
async def list_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Display list items."""
    # Parse arguments and flags
    options, positional = _parse_list_options(args)

    # Get list service from context
    list_service = ctx.list_service

    # Execute query
    items = await list_service.get_items(
        list_name=positional[0] if positional else None,
        **options,
    )

    # Format output
    table = _format_items_table(items, options)

    return CommandResult(success=True, message=table)
```

### Argument Parsing

All list commands use consistent flag parsing:

```python
def _parse_list_flags(args: tuple[str, ...]) -> tuple[dict, list[str]]:
    """
    Parse command flags and return options dict + positional args.

    Supports both short (-p high) and long (--priority=high) forms.
    """
    options = {
        "priority": None,
        "status": ["pending", "active", "in_progress"],  # Default excludes done
        "category": None,
        "tag": None,
        "sort_by": "priority",
        "order": "asc",
    }
    positional = []

    i = 0
    while i < len(args):
        arg = args[i]

        if arg.startswith("--"):
            # Long form: --priority=high
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                _apply_option(options, key, value)
                i += 1
            else:
                # Long form: --priority high
                key = arg[2:]
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    _apply_option(options, key, args[i + 1])
                    i += 2
                else:
                    i += 1

        elif arg.startswith("-") and len(arg) == 2:
            # Short form: -p high
            flag = arg[1]
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                _apply_short_option(options, flag, args[i + 1])
                i += 2
            else:
                _apply_short_option(options, flag, None)
                i += 1

        else:
            # Positional argument
            positional.append(arg)
            i += 1

    return options, positional

def _apply_short_option(options: dict, flag: str, value: str | None) -> None:
    """Apply short flag to options dict."""
    flag_map = {
        "s": "sort_by",
        "o": "order",
        "S": "status",
        "p": "priority",
        "c": "category",
        "t": "tag",
        "d": "description",
        "f": "force",
        "T": "add_tag",
        "R": "remove_tag",
    }

    key = flag_map.get(flag)
    if key:
        if key == "status" and value:
            # Status can be "all" or specific value
            if value == "all":
                options[key] = ["pending", "active", "in_progress", "done"]
            else:
                options[key] = [value]
        elif key == "force":
            options[key] = True
        elif value:
            options[key] = value
```

## Storage Integration

### Bootstrap Setup

In `cato/bootstrap.py`:

```python
async def create_storage(config: CatoConfig) -> Storage:
    """Create and initialize storage."""
    db = Database(expand_path(config.storage.database_path))
    await db.connect()

    # Create repositories
    list_repo = ListRepository(db)
    item_repo = ListItemRepository(db)

    # Create service
    list_service = ListService(list_repo, item_repo)

    storage = Storage(
        db=db,
        lists=list_service,
    )

    return storage
```

### Storage Class

```python
class Storage:
    """Unified storage access."""

    def __init__(
        self,
        db: Database,
        lists: ListService,
    ) -> None:
        self._db = db
        self.lists = lists

    async def connect(self) -> None:
        """Connect to database."""
        await self._db.connect()

    async def close(self) -> None:
        """Close database connection."""
        await self._db.close()
```

## Database Migrations

Since no backward compatibility is required, use a simple init migration:

```python
MIGRATIONS = [
    Migration(
        name="001_lists_schema",
        sql="""
        -- Lists table
        CREATE TABLE IF NOT EXISTS lists (
            name TEXT PRIMARY KEY,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_lists_created ON lists(created_at);

        -- List items table
        CREATE TABLE IF NOT EXISTS list_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'medium',
            category TEXT,
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (list_name) REFERENCES lists(name) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_list_items_list_name ON list_items(list_name);
        CREATE INDEX IF NOT EXISTS idx_list_items_status ON list_items(status);
        CREATE INDEX IF NOT EXISTS idx_list_items_priority ON list_items(priority);
        CREATE INDEX IF NOT EXISTS idx_list_items_category ON list_items(category);
        CREATE INDEX IF NOT EXISTS idx_list_items_created ON list_items(created_at);
        """,
    ),
]
```

## Display Formatting

### Table Rendering

Use Rich library for formatted output:

```python
from rich.table import Table
from io import StringIO
from rich.console import Console

def format_items_table(
    items: list[ListItem],
    list_name: str | None = None,
    sort_by: str = "priority",
) -> str:
    """
    Format items as Rich table.

    Parameters
    ----------
    items : list[ListItem]
        Items to display.
    list_name : str | None
        List name for title (None for multi-list view).
    sort_by : str
        Sort field (for title display).

    Returns
    -------
    str
        Rendered table string.
    """
    title = f"List: {list_name}" if list_name else "All Lists"
    title += f" ({len(items)} items) - sorted by {sort_by}"

    table = Table(title=title)
    table.add_column("ID", width=5)
    table.add_column("S", width=3)
    table.add_column("Priority", width=10)
    table.add_column("Category", width=12)
    table.add_column("Description", width=30)
    table.add_column("Tags", width=15)

    for item in items:
        table.add_row(
            item.display_id,
            _format_status(item.status),
            _format_priority(item.priority),
            (item.category or "")[:12],
            item.description[:30],
            ",".join(item.tags[:2]) + (f"+{len(item.tags)-2}" if len(item.tags) > 2 else ""),
        )

    # Render to string
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=False, width=80)
    console.print(table)
    return buffer.getvalue()

def _format_status(status: str) -> str:
    """Format status as emoji."""
    status_map = {
        "pending": "⚪",
        "active": "🔵",
        "in_progress": "🟡",
        "done": "✅",
    }
    return status_map.get(status, "❓")

def _format_priority(priority: str) -> str:
    """Format priority as emoji + text."""
    priority_map = {
        "urgent": "🔥 URG",
        "high": "⚡ HIGH",
        "medium": "● MED",
        "low": "○ LOW",
    }
    return priority_map.get(priority, priority)
```

## Error Handling

### Custom Exceptions

```python
class ListError(CatoError):
    """Base exception for list operations."""
    pass

class ListNotFoundError(ListError):
    """List not found."""
    pass

class ItemNotFoundError(ListError):
    """Item not found."""
    pass

class ListExistsError(ListError):
    """List already exists."""
    pass
```

### Command Error Handling

```python
@command(name="add", aliases=["a"])
async def add_command(ctx: CommandContext, *args: str) -> CommandResult:
    """Add item to list."""
    try:
        # Parse and validate
        if len(args) < 2:
            return CommandResult(
                success=False,
                message="Usage: /add <list> <description> [-p priority] [-c category]"
            )

        # Execute
        item = await ctx.list_service.add_item(...)

        return CommandResult(
            success=True,
            message=f"✓ Added item #{item.display_id} to {item.list_name}"
        )

    except ListError as e:
        return CommandResult(success=False, message=f"✗ {e}")
    except Exception as e:
        logger.exception("Unexpected error in add command")
        return CommandResult(
            success=False,
            message=f"✗ Unexpected error: {e}"
        )
```

## Testing Strategy

### Unit Tests

```python
# Test repository layer
async def test_list_item_repository_create():
    db = await create_test_db()
    repo = ListItemRepository(db)

    item = ListItem(
        list_name="test",
        description="Test item",
        priority="high",
    )

    item_id = await repo.create(item)
    assert item_id > 0

    retrieved = await repo.get(item_id)
    assert retrieved.description == "Test item"
    assert retrieved.priority == "high"

# Test service layer
async def test_list_service_add_item():
    list_service = create_test_list_service()

    item = await list_service.add_item(
        list_name="todo",
        description="Test task",
        priority="urgent",
    )

    assert item.id is not None
    assert item.priority == "urgent"
```

### Integration Tests

```python
async def test_add_and_retrieve_items():
    """Test full flow from add to retrieve."""
    storage = await create_test_storage()

    # Add items
    item1 = await storage.lists.add_item("todo", "Task 1", priority="high")
    item2 = await storage.lists.add_item("todo", "Task 2", priority="low")

    # Retrieve sorted by priority
    items = await storage.lists.get_items(
        list_name="todo",
        sort_by="priority",
        order="asc",
    )

    assert len(items) == 2
    assert items[0].id == item1.id  # High priority first
    assert items[1].id == item2.id
```

## Performance Considerations

### Indexes

All query patterns are supported by indexes:
- Filter by list_name: `idx_list_items_list_name`
- Filter by status: `idx_list_items_status`
- Sort by priority: `idx_list_items_priority`
- Filter by category: `idx_list_items_category`
- Sort by created: `idx_list_items_created`

### Query Optimization

1. **Avoid N+1 queries**: Fetch all items in one query
2. **Use CASE for priority sorting**: Avoids Python-side sorting
3. **JSON functions for tags**: SQLite JSON1 extension
4. **Connection pooling**: Single connection for session

### Scalability

For large lists (>1000 items):
- Add pagination support
- Consider full-text search index on description
- Add archiving mechanism for old done items

## File Organization

```
cato/
├── storage/
│   ├── database.py           # Database connection class
│   └── repositories/
│       ├── base.py           # Base repository protocol
│       └── lists.py          # ListRepository, ListItemRepository
│
├── services/
│   └── lists.py              # ListService (business logic)
│
├── commands/
│   └── lists.py              # All list commands (/add, /list, etc.)
│
└── core/
    └── types.py              # List, ListItem data models
```

## Configuration

Add to storage config:

```yaml
storage:
  database_path: "~/.local/share/cato/cato.db"

lists:
  default_priority: "medium"
  default_status: "pending"
  max_description_length: 500
  display_width: 80
```

## Summary

This implementation provides:

1. **Clean Schema**: Two tables with global IDs
2. **Type Safety**: Pydantic models throughout
3. **Repository Pattern**: Clear data access layer
4. **Service Layer**: Business logic separation
5. **Command Layer**: Consistent command interface
6. **Rich Output**: Formatted tables with color
7. **Extensible**: Metadata field for future additions
8. **Testable**: Clear interfaces at each layer

The system replaces the old separate Tasks and Lists with a unified, simpler implementation that's easier to maintain and extend.

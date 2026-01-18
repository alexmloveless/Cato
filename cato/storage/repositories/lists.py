"""Unified list and list item repository implementations."""

import json
import logging
from datetime import datetime
from typing import Any

from cato.core.types import List, ListItem
from cato.storage.database import Database

logger = logging.getLogger(__name__)


class ListRepository:
    """
    Repository for list operations.

    Parameters
    ----------
    db : Database
        Database connection.
    """

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
        logger.info(f"Created list: {lst.name}")
        return lst.name

    async def delete_list(self, name: str) -> None:
        """Delete list by name (cascades to items)."""
        await self._db.execute("DELETE FROM lists WHERE name = ?", (name,))
        logger.info(f"Deleted list: {name}")

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

    def _row_to_list(self, row: dict[str, Any]) -> List:
        """Convert DB row to List entity."""
        return List(
            name=row["name"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )


class ListItemRepository:
    """
    Repository for list item operations.

    Parameters
    ----------
    db : Database
        Database connection.
    """

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
            Sort field (priority, status, category, created_at, id).
        order : str
            Sort order (asc, desc).

        Returns
        -------
        list[ListItem]
            Matching items.
        """
        query = "SELECT * FROM list_items WHERE 1=1"
        params: list[Any] = []

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
            query += " AND EXISTS (SELECT 1 FROM json_each(list_items.tags) WHERE value = ?)"
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
        item_id = cursor.lastrowid
        logger.info(f"Created list item: {item_id}")
        return item_id

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
        logger.info(f"Updated list item: {item.id}")

    async def delete(self, id: int) -> None:
        """Delete item by ID."""
        await self._db.execute("DELETE FROM list_items WHERE id = ?", (id,))
        logger.info(f"Deleted list item: {id}")

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
        cursor = await self._db.execute(
            "DELETE FROM list_items WHERE list_name = ? AND status = ?",
            (list_name, status)
        )
        # SQLite doesn't have rowcount on cursor, so we need to check rows affected
        return cursor.rowcount if hasattr(cursor, 'rowcount') else 0

    def _row_to_item(self, row: dict[str, Any]) -> ListItem:
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

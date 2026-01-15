"""List and list item repository implementations."""

import json
import logging
from datetime import datetime
from typing import Any

from cato.storage.database import Database
from cato.storage.repositories.base import List, ListItem

logger = logging.getLogger(__name__)


class ListRepository:
    """
    SQLite-backed list repository.
    
    Parameters
    ----------
    db : Database
        Database connection.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> List | None:
        """
        Get list by ID.
        
        Parameters
        ----------
        id : str
            List ID.
        
        Returns
        -------
        List | None
            List if found, None otherwise.
        """
        row = await self._db.fetchone("SELECT * FROM lists WHERE id = ?", (id,))
        return self._row_to_list(row) if row else None
    
    async def get_by_name(self, name: str) -> List | None:
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
        row = await self._db.fetchone("SELECT * FROM lists WHERE name = ?", (name,))
        return self._row_to_list(row) if row else None
    
    async def get_all(self) -> list[List]:
        """
        Get all lists.
        
        Returns
        -------
        list[List]
            List of all lists.
        """
        rows = await self._db.fetchall("SELECT * FROM lists ORDER BY created_at DESC")
        return [self._row_to_list(row) for row in rows]
    
    async def create(self, lst: List) -> str:
        """
        Create new list.
        
        Parameters
        ----------
        lst : List
            List to create.
        
        Returns
        -------
        str
            Created list ID.
        """
        await self._db.execute(
            """
            INSERT INTO lists (id, name, description, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                lst.id,
                lst.name,
                lst.description,
                lst.created_at.isoformat(),
                lst.updated_at.isoformat(),
                json.dumps(lst.metadata) if lst.metadata else None,
            ),
        )
        logger.info(f"Created list: {lst.id}")
        return lst.id
    
    async def update(self, lst: List) -> None:
        """
        Update existing list.
        
        Parameters
        ----------
        lst : List
            List to update.
        """
        lst.updated_at = datetime.now()
        
        await self._db.execute(
            """
            UPDATE lists SET name = ?, description = ?, updated_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                lst.name,
                lst.description,
                lst.updated_at.isoformat(),
                json.dumps(lst.metadata) if lst.metadata else None,
                lst.id,
            ),
        )
        logger.info(f"Updated list: {lst.id}")
    
    async def delete(self, id: str) -> None:
        """
        Delete list by ID.
        
        Cascades to all list items due to foreign key constraint.
        
        Parameters
        ----------
        id : str
            List ID to delete.
        """
        await self._db.execute("DELETE FROM lists WHERE id = ?", (id,))
        logger.info(f"Deleted list: {id}")
    
    def _row_to_list(self, row: dict[str, Any]) -> List:
        """Convert database row to List entity."""
        return List(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )


class ListItemRepository:
    """
    SQLite-backed list item repository.
    
    Parameters
    ----------
    db : Database
        Database connection.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> ListItem | None:
        """
        Get list item by ID.
        
        Parameters
        ----------
        id : str
            Item ID.
        
        Returns
        -------
        ListItem | None
            Item if found, None otherwise.
        """
        row = await self._db.fetchone("SELECT * FROM list_items WHERE id = ?", (id,))
        return self._row_to_item(row) if row else None
    
    async def get_all(self, list_id: str) -> list[ListItem]:
        """
        Get all items in a list.
        
        Parameters
        ----------
        list_id : str
            Parent list ID.
        
        Returns
        -------
        list[ListItem]
            List of items ordered by position.
        """
        rows = await self._db.fetchall(
            "SELECT * FROM list_items WHERE list_id = ? ORDER BY position ASC",
            (list_id,),
        )
        return [self._row_to_item(row) for row in rows]
    
    async def create(self, item: ListItem) -> str:
        """
        Create new list item.
        
        Parameters
        ----------
        item : ListItem
            Item to create.
        
        Returns
        -------
        str
            Created item ID.
        """
        await self._db.execute(
            """
            INSERT INTO list_items (
                id, list_id, content, checked, position,
                created_at, updated_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                item.list_id,
                item.content,
                1 if item.checked else 0,
                item.position,
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
                json.dumps(item.metadata) if item.metadata else None,
            ),
        )
        logger.info(f"Created list item: {item.id}")
        return item.id
    
    async def update(self, item: ListItem) -> None:
        """
        Update existing list item.
        
        Parameters
        ----------
        item : ListItem
            Item to update.
        """
        item.updated_at = datetime.now()
        
        await self._db.execute(
            """
            UPDATE list_items SET
                content = ?, checked = ?, position = ?, updated_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                item.content,
                1 if item.checked else 0,
                item.position,
                item.updated_at.isoformat(),
                json.dumps(item.metadata) if item.metadata else None,
                item.id,
            ),
        )
        logger.info(f"Updated list item: {item.id}")
    
    async def delete(self, id: str) -> None:
        """
        Delete list item by ID.
        
        Parameters
        ----------
        id : str
            Item ID to delete.
        """
        await self._db.execute("DELETE FROM list_items WHERE id = ?", (id,))
        logger.info(f"Deleted list item: {id}")
    
    def _row_to_item(self, row: dict[str, Any]) -> ListItem:
        """Convert database row to ListItem entity."""
        return ListItem(
            id=row["id"],
            list_id=row["list_id"],
            content=row["content"],
            checked=bool(row["checked"]),
            position=row["position"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )

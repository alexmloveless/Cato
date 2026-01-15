"""Task repository implementation."""

import json
import logging
from datetime import datetime
from typing import Any

from cato.storage.database import Database
from cato.storage.repositories.base import Task

logger = logging.getLogger(__name__)


class TaskRepository:
    """
    SQLite-backed task repository.
    
    Provides CRUD operations for Task entities with filtering and sorting support.
    
    Parameters
    ----------
    db : Database
        Database connection.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> Task | None:
        """
        Get task by ID.
        
        Parameters
        ----------
        id : str
            Task ID.
        
        Returns
        -------
        Task | None
            Task if found, None otherwise.
        """
        row = await self._db.fetchone("SELECT * FROM tasks WHERE id = ?", (id,))
        return self._row_to_task(row) if row else None
    
    async def get_all(
        self,
        status: str | None = None,
        category: str | None = None,
        priority: str | None = None,
        sort_by: str = "created_at",
        order: str = "asc",
    ) -> list[Task]:
        """
        Get tasks with optional filters.
        
        Parameters
        ----------
        status : str | None, optional
            Filter by status.
        category : str | None, optional
            Filter by category.
        priority : str | None, optional
            Filter by priority.
        sort_by : str, optional
            Sort field (default: created_at).
        order : str, optional
            Sort order: asc or desc (default: asc).
        
        Returns
        -------
        list[Task]
            List of matching tasks.
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list[Any] = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        # Validate sort field to prevent SQL injection
        valid_sorts = {"created_at", "updated_at", "priority", "due_date", "title"}
        if sort_by not in valid_sorts:
            sort_by = "created_at"
        
        order_dir = "DESC" if order.lower() == "desc" else "ASC"
        query += f" ORDER BY {sort_by} {order_dir}"
        
        rows = await self._db.fetchall(query, tuple(params))
        return [self._row_to_task(row) for row in rows]
    
    async def create(self, task: Task) -> str:
        """
        Create new task.
        
        Parameters
        ----------
        task : Task
            Task to create.
        
        Returns
        -------
        str
            Created task ID.
        """
        await self._db.execute(
            """
            INSERT INTO tasks (
                id, title, description, status, priority, category,
                due_date, created_at, updated_at, completed_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.id,
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
            ),
        )
        logger.info(f"Created task: {task.id}")
        return task.id
    
    async def update(self, task: Task) -> None:
        """
        Update existing task.
        
        Parameters
        ----------
        task : Task
            Task to update.
        """
        # Update timestamp
        task.updated_at = datetime.now()
        
        await self._db.execute(
            """
            UPDATE tasks SET
                title = ?, description = ?, status = ?, priority = ?,
                category = ?, due_date = ?, updated_at = ?,
                completed_at = ?, metadata = ?
            WHERE id = ?
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task.category,
                task.due_date.isoformat() if task.due_date else None,
                task.updated_at.isoformat(),
                task.completed_at.isoformat() if task.completed_at else None,
                json.dumps(task.metadata) if task.metadata else None,
                task.id,
            ),
        )
        logger.info(f"Updated task: {task.id}")
    
    async def delete(self, id: str) -> None:
        """
        Delete task by ID.
        
        Parameters
        ----------
        id : str
            Task ID to delete.
        """
        await self._db.execute("DELETE FROM tasks WHERE id = ?", (id,))
        logger.info(f"Deleted task: {id}")
    
    def _row_to_task(self, row: dict[str, Any]) -> Task:
        """
        Convert database row to Task entity.
        
        Parameters
        ----------
        row : dict[str, Any]
            Database row.
        
        Returns
        -------
        Task
            Task entity.
        """
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            priority=row["priority"],
            category=row["category"],
            due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            completed_at=(
                datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None
            ),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )

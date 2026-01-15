"""Productivity service for task and list management."""

import logging
from typing import Literal

from cato.storage.repositories.base import Task, List, ListItem
from cato.storage.service import Storage

logger = logging.getLogger(__name__)


class ProductivityService:
    """
    Service for managing tasks and lists.
    
    Wraps repository methods with business logic and formatting.
    
    Parameters
    ----------
    storage : Storage
        Storage service with repository access.
    """
    
    def __init__(self, storage: Storage) -> None:
        self._storage = storage
        logger.info("ProductivityService initialized")
    
    async def get_tasks(
        self,
        category: str | None = None,
        priority: str | None = None,
        status: str | list[str] | None = None,
        sort_by: str = "created_at",
        order: Literal["asc", "desc"] = "desc",
    ) -> list[Task]:
        """
        Get tasks with filtering and sorting.
        
        Parameters
        ----------
        category : str | None, optional
            Filter by category.
        priority : str | None, optional
            Filter by priority (urgent, high, medium, low).
        status : str | list[str] | None, optional
            Filter by status. Can be single status or list.
            Default behavior: ["active", "in_progress"] if None.
        sort_by : str, default="created_at"
            Sort field (created_at, priority, category, due_date, title).
        order : Literal["asc", "desc"], default="desc"
            Sort order.
        
        Returns
        -------
        list[Task]
            Filtered and sorted tasks.
        """
        # Handle default status filter
        if status is None:
            status = ["active", "in_progress"]
        
        # Convert single status to list
        if isinstance(status, str):
            status = [status]
        
        # If multiple statuses, fetch separately and combine
        if len(status) > 1:
            all_tasks = []
            for s in status:
                tasks = await self._storage.tasks.get_all(
                    status=s,
                    category=category,
                    priority=priority,
                    sort_by=sort_by,
                    order=order,
                )
                all_tasks.extend(tasks)
            return all_tasks
        else:
            # Single status or empty list
            return await self._storage.tasks.get_all(
                status=status[0] if status else None,
                category=category,
                priority=priority,
                sort_by=sort_by,
                order=order,
            )
    
    async def get_task(self, task_id: str) -> Task | None:
        """
        Get single task by ID.
        
        Parameters
        ----------
        task_id : str
            Task ID.
        
        Returns
        -------
        Task | None
            Task if found, None otherwise.
        """
        return await self._storage.tasks.get(task_id)
    
    async def get_all_lists(self) -> list[List]:
        """
        Get all lists.
        
        Returns
        -------
        list[List]
            All lists.
        """
        return await self._storage.lists.get_all()
    
    async def get_list(self, list_id_or_name: str) -> List | None:
        """
        Get list by ID or name.
        
        Parameters
        ----------
        list_id_or_name : str
            List ID or name.
        
        Returns
        -------
        List | None
            List if found, None otherwise.
        """
        # Try by ID first
        lst = await self._storage.lists.get(list_id_or_name)
        if lst:
            return lst
        
        # Try by name
        return await self._storage.lists.get_by_name(list_id_or_name)
    
    async def get_list_items(self, list_id: str) -> list[ListItem]:
        """
        Get all items in a list.
        
        Parameters
        ----------
        list_id : str
            List ID.
        
        Returns
        -------
        list[ListItem]
            List items ordered by position.
        """
        return await self._storage.list_items.get_all(list_id)
    
    async def count_list_items(self, list_id: str) -> int:
        """
        Count items in a list.
        
        Parameters
        ----------
        list_id : str
            List ID.
        
        Returns
        -------
        int
            Number of items in list.
        """
        items = await self.get_list_items(list_id)
        return len(items)

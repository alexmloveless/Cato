"""List management service with business logic."""

import logging
from datetime import datetime

from cato.core.types import List, ListItem
from cato.storage.repositories.lists import ListItemRepository, ListRepository

logger = logging.getLogger(__name__)


class ListService:
    """
    Service for list operations (business logic).

    Parameters
    ----------
    list_repo : ListRepository
        Repository for list operations.
    item_repo : ListItemRepository
        Repository for list item operations.
    """

    def __init__(
        self,
        list_repo: ListRepository,
        item_repo: ListItemRepository,
    ) -> None:
        self._lists = list_repo
        self._items = item_repo
        logger.info("ListService initialized")

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
        logger.info(f"Created list: {name}")
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
        logger.info(f"Deleted list: {name} ({item_count} items)")
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
        logger.info(f"Added item #{item_id:03d} to {list_name}")
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
        logger.info(f"Updated item #{item.display_id}")
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
        logger.info(f"Removed item #{item.display_id} from {item.list_name}")
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

        logger.info(f"Moved item #{item.display_id} from {old_list} to {target_list}")
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
            logger.info(f"Cleared {count} {status} items from {list_name}")
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
            logger.info(f"Cleared all {count} items from {list_name}")
            return True, f"Cleared all {count} items from {list_name}"

    async def get_items(
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
        Get items with filters and sorting.

        Parameters
        ----------
        list_name : str | None
            Filter by list name.
        status : list[str] | None
            Filter by status values. Default: ["pending", "active", "in_progress"].
        priority : str | None
            Filter by priority.
        category : str | None
            Filter by category.
        tag : str | None
            Filter by tag.
        sort_by : str
            Sort field.
        order : str
            Sort order.

        Returns
        -------
        list[ListItem]
            Matching items.
        """
        # Default status filter excludes done items
        if status is None:
            status = ["pending", "active", "in_progress"]

        return await self._items.get_all(
            list_name=list_name,
            status=status,
            priority=priority,
            category=category,
            tag=tag,
            sort_by=sort_by,
            order=order,
        )

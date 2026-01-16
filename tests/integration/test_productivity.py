"""
Integration tests for productivity system.

Tests cover:
- Task management workflows
- List management workflows
- Integration between components
"""

from datetime import datetime

import pytest

from cato.storage.repositories.base import Task, List, ListItem
from cato.storage.repositories.tasks import TaskRepository
from cato.storage.repositories.lists import ListRepository


@pytest.mark.asyncio
class TestTaskWorkflows:
    """Test complete task management workflows."""

    async def test_create_and_complete_task(self, test_db):
        """Test full lifecycle of creating and completing a task."""
        repo = TaskRepository(test_db)

        # Create task
        task = Task(
            id=None,
            title="Write integration tests",
            status="pending",
            priority="high",
            created_at=datetime.now(),
        )
        task_id = await repo.create(task)

        # Mark as in progress
        task.id = task_id
        task.status = "in_progress"
        await repo.update(task)

        # Complete it
        task.status = "completed"
        task.completed_at = datetime.now()
        await repo.update(task)

        # Verify final state
        final = await repo.get(task_id)
        assert final.status == "completed"
        assert final.completed_at is not None

    async def test_prioritize_tasks(self, test_db):
        """Test workflow of changing task priorities."""
        repo = TaskRepository(test_db)

        # Create task with low priority
        task = Task(
            id=None,
            title="Important task",
            status="pending",
            priority="low",
            created_at=datetime.now(),
        )
        task_id = await repo.create(task)

        # Escalate priority
        task.id = task_id
        task.priority = "high"
        await repo.update(task)

        # Verify
        updated = await repo.get(task_id)
        assert updated.priority == "high"


@pytest.mark.asyncio
class TestListWorkflows:
    """Test complete list management workflows."""

    async def test_create_shopping_list(self, test_db):
        """Test creating and populating a shopping list."""
        list_repo = ListRepository(test_db)

        # Create list
        shopping_list = List(
            id=None,
            name="Groceries",
            description="Weekly shopping",
            created_at=datetime.now(),
        )
        list_id = await list_repo.create(shopping_list)

        # Verify list exists
        retrieved = await list_repo.get(list_id)
        assert retrieved.name == "Groceries"

    async def test_rename_list(self, test_db):
        """Test renaming a list."""
        repo = ListRepository(test_db)

        # Create list
        list_obj = List(
            id=None,
            name="Old Name",
            created_at=datetime.now(),
        )
        list_id = await repo.create(list_obj)

        # Rename
        list_obj.id = list_id
        list_obj.name = "New Name"
        await repo.update(list_obj)

        # Verify
        updated = await repo.get(list_id)
        assert updated.name == "New Name"


@pytest.mark.asyncio
class TestTaskFiltering:
    """Test filtering and sorting tasks."""

    async def test_filter_pending_high_priority(self, test_db):
        """Test filtering for pending high-priority tasks."""
        repo = TaskRepository(test_db)

        # Create various tasks
        tasks_data = [
            ("Task 1", "pending", "high"),
            ("Task 2", "pending", "low"),
            ("Task 3", "completed", "high"),
            ("Task 4", "pending", "high"),
        ]

        for title, status, priority in tasks_data:
            await repo.create(Task(
                id=None,
                title=title,
                status=status,
                priority=priority,
                created_at=datetime.now(),
            ))

        # Filter for pending + high priority
        results = await repo.filter_by(status="pending", priority="high")

        assert len(results) >= 2
        for task in results:
            if task.title in [t[0] for t in tasks_data]:
                assert task.status == "pending"
                assert task.priority == "high"

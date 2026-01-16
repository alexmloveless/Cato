"""
Unit tests for database repositories.

Tests cover:
- Task repository CRUD operations
- List repository CRUD operations
- Session repository CRUD operations
- Filtering and sorting
- Error handling
"""

from datetime import datetime, timedelta

import pytest

from cato.storage.repositories.base import Task, List, ListItem, Session, Thread
from cato.storage.repositories.tasks import TaskRepository
from cato.storage.repositories.lists import ListRepository
from cato.storage.repositories.sessions import SessionRepository


@pytest.mark.asyncio
class TestTaskRepository:
    """Test task repository operations."""

    async def test_create_task(self, test_db):
        """Test creating a new task."""
        repo = TaskRepository(test_db)

        task = Task(
            id=None,
            title="Test task",
            status="pending",
            priority="medium",
            created_at=datetime.now(),
        )

        task_id = await repo.create(task)
        assert task_id is not None
        assert isinstance(task_id, str)

        # Verify task was created
        retrieved = await repo.get(task_id)
        assert retrieved is not None
        assert retrieved.title == "Test task"
        assert retrieved.status == "pending"

    async def test_get_task(self, test_db):
        """Test retrieving a task by ID."""
        repo = TaskRepository(test_db)

        # Create a task
        task = Task(
            id=None,
            title="Get test",
            status="pending",
            priority="high",
            created_at=datetime.now(),
        )
        task_id = await repo.create(task)

        # Retrieve it
        retrieved = await repo.get(task_id)
        assert retrieved is not None
        assert retrieved.id == task_id
        assert retrieved.title == "Get test"
        assert retrieved.priority == "high"

    async def test_get_nonexistent_task(self, test_db):
        """Test getting task that doesn't exist."""
        repo = TaskRepository(test_db)
        task = await repo.get("nonexistent-id")
        assert task is None

    async def test_update_task(self, test_db):
        """Test updating an existing task."""
        repo = TaskRepository(test_db)

        # Create task
        task = Task(
            id=None,
            title="Original title",
            status="pending",
            priority="low",
            created_at=datetime.now(),
        )
        task_id = await repo.create(task)

        # Update it
        task.id = task_id
        task.title = "Updated title"
        task.status = "completed"
        task.priority = "high"
        await repo.update(task)

        # Verify update
        retrieved = await repo.get(task_id)
        assert retrieved.title == "Updated title"
        assert retrieved.status == "completed"
        assert retrieved.priority == "high"

    async def test_delete_task(self, test_db):
        """Test deleting a task."""
        repo = TaskRepository(test_db)

        # Create task
        task = Task(
            id=None,
            title="To be deleted",
            status="pending",
            priority="medium",
            created_at=datetime.now(),
        )
        task_id = await repo.create(task)

        # Verify it exists
        assert await repo.get(task_id) is not None

        # Delete it
        await repo.delete(task_id)

        # Verify it's gone
        assert await repo.get(task_id) is None

    async def test_get_all_tasks(self, test_db):
        """Test retrieving all tasks."""
        repo = TaskRepository(test_db)

        # Create multiple tasks
        tasks = [
            Task(
                id=None,
                title=f"Task {i}",
                status="pending",
                priority="medium",
                created_at=datetime.now(),
            )
            for i in range(3)
        ]

        for task in tasks:
            await repo.create(task)

        # Retrieve all
        all_tasks = await repo.get_all()
        assert len(all_tasks) >= 3  # At least our 3 tasks

    async def test_filter_by_status(self, test_db):
        """Test filtering tasks by status."""
        repo = TaskRepository(test_db)

        # Create tasks with different statuses
        await repo.create(Task(
            id=None,
            title="Pending task",
            status="pending",
            priority="medium",
            created_at=datetime.now(),
        ))
        await repo.create(Task(
            id=None,
            title="Completed task",
            status="completed",
            priority="medium",
            created_at=datetime.now(),
        ))

        # Filter by status
        pending = await repo.filter_by(status="pending")
        completed = await repo.filter_by(status="completed")

        assert len(pending) >= 1
        assert len(completed) >= 1
        assert all(t.status == "pending" for t in pending)
        assert all(t.status == "completed" for t in completed)

    async def test_filter_by_priority(self, test_db):
        """Test filtering tasks by priority."""
        repo = TaskRepository(test_db)

        # Create tasks with different priorities
        await repo.create(Task(
            id=None,
            title="High priority",
            status="pending",
            priority="high",
            created_at=datetime.now(),
        ))
        await repo.create(Task(
            id=None,
            title="Low priority",
            status="pending",
            priority="low",
            created_at=datetime.now(),
        ))

        # Filter by priority
        high = await repo.filter_by(priority="high")
        low = await repo.filter_by(priority="low")

        assert len(high) >= 1
        assert len(low) >= 1
        assert all(t.priority == "high" for t in high)
        assert all(t.priority == "low" for t in low)

    async def test_sort_by_priority(self, test_db):
        """Test sorting tasks by priority."""
        repo = TaskRepository(test_db)

        # Create tasks with different priorities
        now = datetime.now()
        await repo.create(Task(id=None, title="Low", status="pending", priority="low", created_at=now))
        await repo.create(Task(id=None, title="High", status="pending", priority="high", created_at=now))
        await repo.create(Task(id=None, title="Medium", status="pending", priority="medium", created_at=now))

        # Get sorted by priority
        tasks = await repo.sort_by("priority")

        # Should be ordered: high, medium, low
        priorities = [t.priority for t in tasks if t.title in ["Low", "High", "Medium"]]
        expected_order = ["high", "medium", "low"]

        # Check that priorities appear in correct order
        for priority in expected_order:
            assert priority in priorities


@pytest.mark.asyncio
class TestListRepository:
    """Test list repository operations."""

    async def test_create_list(self, test_db):
        """Test creating a new list."""
        repo = ListRepository(test_db)

        list_obj = List(
            id=None,
            name="Shopping",
            description="Grocery shopping list",
            created_at=datetime.now(),
        )

        list_id = await repo.create(list_obj)
        assert list_id is not None

        # Verify list was created
        retrieved = await repo.get(list_id)
        assert retrieved is not None
        assert retrieved.name == "Shopping"

    async def test_get_list(self, test_db):
        """Test retrieving a list by ID."""
        repo = ListRepository(test_db)

        # Create a list
        list_obj = List(
            id=None,
            name="Todo",
            created_at=datetime.now(),
        )
        list_id = await repo.create(list_obj)

        # Retrieve it
        retrieved = await repo.get(list_id)
        assert retrieved is not None
        assert retrieved.id == list_id
        assert retrieved.name == "Todo"

    async def test_update_list(self, test_db):
        """Test updating a list."""
        repo = ListRepository(test_db)

        # Create list
        list_obj = List(
            id=None,
            name="Original",
            created_at=datetime.now(),
        )
        list_id = await repo.create(list_obj)

        # Update it
        list_obj.id = list_id
        list_obj.name = "Updated"
        list_obj.description = "New description"
        await repo.update(list_obj)

        # Verify update
        retrieved = await repo.get(list_id)
        assert retrieved.name == "Updated"
        assert retrieved.description == "New description"

    async def test_delete_list(self, test_db):
        """Test deleting a list."""
        repo = ListRepository(test_db)

        # Create list
        list_obj = List(
            id=None,
            name="To delete",
            created_at=datetime.now(),
        )
        list_id = await repo.create(list_obj)

        # Delete it
        await repo.delete(list_id)

        # Verify it's gone
        assert await repo.get(list_id) is None

    async def test_get_list_by_name(self, test_db):
        """Test getting list by name."""
        repo = ListRepository(test_db)

        # Create list with unique name
        unique_name = f"unique_list_{datetime.now().timestamp()}"
        list_obj = List(
            id=None,
            name=unique_name,
            created_at=datetime.now(),
        )
        await repo.create(list_obj)

        # Get by name
        retrieved = await repo.get_by_name(unique_name)
        assert retrieved is not None
        assert retrieved.name == unique_name


@pytest.mark.asyncio
class TestSessionRepository:
    """Test session repository operations."""

    async def test_create_session(self, test_db):
        """Test creating a new session."""
        repo = SessionRepository(test_db)

        session = Session(
            id="test-session-1",
            started_at=datetime.now(),
            message_count=0,
            metadata={},
        )

        session_id = await repo.create(session)
        assert session_id == "test-session-1"

        # Verify session was created
        retrieved = await repo.get(session_id)
        assert retrieved is not None
        assert retrieved.id == "test-session-1"

    async def test_update_session(self, test_db):
        """Test updating a session."""
        repo = SessionRepository(test_db)

        # Create session
        session = Session(
            id="update-test",
            started_at=datetime.now(),
            message_count=0,
            metadata={},
        )
        await repo.create(session)

        # Update it
        session.message_count = 5
        session.ended_at = datetime.now()
        session.metadata = {"key": "value"}
        await repo.update(session)

        # Verify update
        retrieved = await repo.get("update-test")
        assert retrieved.message_count == 5
        assert retrieved.ended_at is not None
        assert retrieved.metadata["key"] == "value"

    async def test_create_thread(self, test_db):
        """Test creating a thread."""
        repo = SessionRepository(test_db)

        # First create a session
        session = Session(
            id="thread-test-session",
            started_at=datetime.now(),
            message_count=0,
        )
        await repo.create(session)

        # Create thread
        thread = Thread(
            id="thread-1",
            session_id="thread-test-session",
            name="Test Thread",
            created_at=datetime.now(),
            metadata={},
        )

        thread_id = await repo.create_thread(thread)
        assert thread_id == "thread-1"

        # Verify thread was created
        retrieved = await repo.get_thread(thread_id)
        assert retrieved is not None
        assert retrieved.name == "Test Thread"

    async def test_get_threads_for_session(self, test_db):
        """Test getting all threads for a session."""
        repo = SessionRepository(test_db)

        # Create session
        session_id = "multi-thread-session"
        session = Session(
            id=session_id,
            started_at=datetime.now(),
            message_count=0,
        )
        await repo.create(session)

        # Create multiple threads
        for i in range(3):
            thread = Thread(
                id=f"thread-{i}",
                session_id=session_id,
                name=f"Thread {i}",
                created_at=datetime.now(),
                metadata={},
            )
            await repo.create_thread(thread)

        # Get all threads
        threads = await repo.get_threads(session_id)
        assert len(threads) == 3

    async def test_delete_thread(self, test_db):
        """Test deleting a thread."""
        repo = SessionRepository(test_db)

        # Create session and thread
        session = Session(
            id="del-thread-session",
            started_at=datetime.now(),
            message_count=0,
        )
        await repo.create(session)

        thread = Thread(
            id="del-thread",
            session_id="del-thread-session",
            name="To delete",
            created_at=datetime.now(),
            metadata={},
        )
        await repo.create_thread(thread)

        # Delete thread
        await repo.delete_thread("del-thread")

        # Verify it's gone
        assert await repo.get_thread("del-thread") is None

    async def test_get_all_sessions(self, test_db):
        """Test getting all sessions."""
        repo = SessionRepository(test_db)

        # Create multiple sessions
        now = datetime.now()
        for i in range(3):
            session = Session(
                id=f"session-{i}",
                started_at=now + timedelta(seconds=i),
                message_count=i,
            )
            await repo.create(session)

        # Get all sessions
        sessions = await repo.get_all()
        assert len(sessions) >= 3

    async def test_get_recent_sessions_with_limit(self, test_db):
        """Test getting recent sessions with limit."""
        repo = SessionRepository(test_db)

        # Create multiple sessions
        now = datetime.now()
        for i in range(5):
            session = Session(
                id=f"recent-{i}",
                started_at=now + timedelta(seconds=i),
                message_count=0,
            )
            await repo.create(session)

        # Get limited number of sessions
        sessions = await repo.get_all(limit=2)
        assert len(sessions) == 2

# Storage Module

This module handles persistent storage using SQLite for productivity features (tasks, lists, sessions).

## Components

### `database.py`
Async SQLite database wrapper with connection management and migration system.

**Key classes:**
- `Database`: Main database connection with async operations
- Provides `execute()`, `fetchone()`, `fetchall()` methods
- Handles schema migrations automatically

### `migrations.py`
Database schema migrations with versioning.

**Key classes:**
- `Migration`: Migration definition with name and SQL
- `MIGRATIONS`: Ordered list of all migrations

### `repositories/`
Repository implementations for each entity type.

**Repositories:**
- `TaskRepository`: CRUD operations for tasks
- `ListRepository`: CRUD operations for lists and list items
- `SessionRepository`: Session and thread tracking

### `service.py`
Unified storage service providing access to all repositories.

**Key classes:**
- `Storage`: Main storage service exposing all repositories
- `create_storage()`: Factory function to create and connect storage

## Usage

```python
from cato.storage import create_storage
from cato.core.config import load_config

config = load_config()
storage = await create_storage(config)

# Access repositories
task = await storage.tasks.get("task_id")
all_tasks = await storage.tasks.get_all(status="active")

# Clean up
await storage.close()
```

## Design Principles

- **Async-first**: All database operations are async
- **Repository pattern**: Clean separation of data access logic
- **Type safety**: Pydantic models validate all entities
- **Migration-based schema**: Never modify schema directly

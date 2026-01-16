# Storage Technical Specification

## Overview
Cato uses SQLite for structured data storage (lists, sessions). The database provides persistent storage for productivity features with a simple data access layer.

## Database Location
```
~/.local/share/cato/cato.db
```

Configurable via `storage.database_path` in config.

## Schema

### Lists Table
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

### List Items Table
```sql
CREATE TABLE IF NOT EXISTS list_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_name TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, active, in_progress, done
    priority TEXT NOT NULL DEFAULT 'medium',  -- urgent, high, medium, low
    category TEXT,
    tags TEXT,                                -- JSON array
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    metadata TEXT,                            -- JSON for extensibility
    FOREIGN KEY (list_name) REFERENCES lists(name) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_list_items_list_name ON list_items(list_name);
CREATE INDEX IF NOT EXISTS idx_list_items_status ON list_items(status);
CREATE INDEX IF NOT EXISTS idx_list_items_priority ON list_items(priority);
CREATE INDEX IF NOT EXISTS idx_list_items_category ON list_items(category);
CREATE INDEX IF NOT EXISTS idx_list_items_created ON list_items(created_at);
```


### Sessions Table
```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    message_count INTEGER DEFAULT 0,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    name TEXT,
    created_at TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
```

## Data Access Layer

### Repository Protocol
```python
from typing import Protocol, TypeVar, Generic

T = TypeVar("T")

class Repository(Protocol[T]):
    """Generic repository protocol for CRUD operations."""
    
    async def get(self, id: str) -> T | None:
        """Get entity by ID."""
        ...
    
    async def get_all(self, **filters) -> list[T]:
        """Get all entities, optionally filtered."""
        ...
    
    async def create(self, entity: T) -> str:
        """Create entity, return ID."""
        ...
    
    async def update(self, entity: T) -> None:
        """Update existing entity."""
        ...
    
    async def delete(self, id: str) -> None:
        """Delete entity by ID."""
        ...
```

### List Repository

See [TECH_SPEC_LISTS.md](TECH_SPEC_LISTS.md) for complete list repository implementation.

**Summary:**
- `ListRepository`: Manages list metadata (name, description, counts)
- `ListItemRepository`: Manages list items with filtering, sorting, and CRUD operations
- Global integer IDs via AUTOINCREMENT
- Support for filtering by status, priority, category, tags
- JSON storage for tags array and metadata

### Database Connection
```python
import aiosqlite
from pathlib import Path

class Database:
    """Async SQLite database wrapper."""
    
    def __init__(self, path: Path) -> None:
        self._path = path
        self._conn: aiosqlite.Connection | None = None
    
    async def connect(self) -> None:
        """Open database connection and initialise schema."""
        # Ensure directory exists
        self._path.parent.mkdir(parents=True, exist_ok=True)
        
        self._conn = await aiosqlite.connect(self._path)
        self._conn.row_factory = aiosqlite.Row
        
        # Enable foreign keys
        await self._conn.execute("PRAGMA foreign_keys = ON")
        
        # Run migrations
        await self._run_migrations()
    
    async def close(self) -> None:
        """Close database connection."""
        if self._conn:
            await self._conn.close()
            self._conn = None
    
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a write query."""
        async with self._conn.execute(query, params):
            await self._conn.commit()
    
    async def fetchone(self, query: str, params: tuple = ()) -> dict | None:
        """Fetch single row."""
        async with self._conn.execute(query, params) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def fetchall(self, query: str, params: tuple = ()) -> list[dict]:
        """Fetch all rows."""
        async with self._conn.execute(query, params) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def _run_migrations(self) -> None:
        """Apply database migrations."""
        # Create migrations table if not exists
        await self._conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                applied_at TEXT NOT NULL
            )
        """)
        await self._conn.commit()
        
        # Get applied migrations
        cursor = await self._conn.execute("SELECT name FROM migrations")
        applied = {row[0] for row in await cursor.fetchall()}
        
        # Apply pending migrations
        for migration in MIGRATIONS:
            if migration.name not in applied:
                await migration.apply(self._conn)
                await self._conn.execute(
                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
                    (migration.name, datetime.now().isoformat()),
                )
                await self._conn.commit()
                logger.info(f"Applied migration: {migration.name}")
```

## Migrations

### Migration Definition
```python
from dataclasses import dataclass

@dataclass
class Migration:
    """
    Database migration.
    
    Note: Uses dataclass as it's internal configuration, not external data.
    """
    name: str
    sql: str
    
    async def apply(self, conn: aiosqlite.Connection) -> None:
        """Apply migration."""
        await conn.executescript(self.sql)


# Ordered list of migrations
MIGRATIONS = [
    Migration(
        name="001_lists_schema",
        sql="""
        CREATE TABLE IF NOT EXISTS lists (
            name TEXT PRIMARY KEY,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_lists_created ON lists(created_at);

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
    Migration(
        name="002_sessions",
        sql="""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            message_count INTEGER DEFAULT 0,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS threads (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            name TEXT,
            created_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );
        """,
    ),
]
```

## Storage Service

### Unified Access
```python
class Storage:
    """
    Unified storage service.

    Provides access to all repositories through a single interface.
    """

    def __init__(self, db: Database) -> None:
        self._db = db
        self.lists = ListService(ListRepository(db), ListItemRepository(db))
        self.sessions = SessionRepository(db)
    
    async def connect(self) -> None:
        """Connect to database."""
        await self._db.connect()
    
    async def close(self) -> None:
        """Close database connection."""
        await self._db.close()


# Usage in bootstrap
async def create_storage(config: CatoConfig) -> Storage:
    """
    Create and connect storage service.
    
    Parameters
    ----------
    config
        Application configuration.
    
    Returns
    -------
    Storage
        Connected storage service.
    """
    db = Database(expand_path(config.storage.database_path))
    storage = Storage(db)
    await storage.connect()
    return storage
```

## Backup

### Automatic Backup
```python
import shutil
from datetime import datetime

class BackupManager:
    """Manage database backups."""
    
    def __init__(self, config: StorageConfig) -> None:
        self._config = config
        self._db_path = expand_path(config.database_path)
        self._backup_dir = self._db_path.parent / "backups"
    
    async def create_backup(self) -> Path:
        """
        Create database backup.
        
        Returns
        -------
        Path
            Path to backup file.
        """
        self._backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self._backup_dir / f"cato_{timestamp}.db"
        
        # Copy database file
        shutil.copy2(self._db_path, backup_path)
        
        # Clean old backups (keep last 7)
        self._cleanup_old_backups(keep=7)
        
        logger.info(f"Database backed up to: {backup_path}")
        return backup_path
    
    def _cleanup_old_backups(self, keep: int) -> None:
        """Remove old backups, keeping the most recent."""
        backups = sorted(
            self._backup_dir.glob("cato_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        
        for backup in backups[keep:]:
            backup.unlink()
            logger.debug(f"Removed old backup: {backup}")
```

## Configuration

### Storage Config
```yaml
storage:
  database_path: "~/.local/share/cato/cato.db"
  backup_enabled: true
  backup_frequency_hours: 24
```

## ID Generation

### List Items

List items use SQLite's AUTOINCREMENT for globally unique integer IDs:

```python
# No manual ID generation needed - SQLite handles it
async def create(self, item: ListItem) -> int:
    """Create item and return auto-generated ID."""
    cursor = await self._db.execute(
        "INSERT INTO list_items (...) VALUES (...)"
    )
    return cursor.lastrowid  # Auto-incrementing integer
```

### Other Entities

For sessions and other entities, use UUID-based IDs:

```python
import uuid

def generate_id() -> str:
    """Generate UUID-based ID."""
    return str(uuid.uuid4())
```

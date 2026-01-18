"""Database migrations for schema management."""

import logging
from dataclasses import dataclass

import aiosqlite

logger = logging.getLogger(__name__)


@dataclass
class Migration:
    """
    Database migration definition.
    
    Parameters
    ----------
    name : str
        Unique migration identifier.
    sql : str
        SQL script to apply.
    
    Notes
    -----
    Uses dataclass as this is internal configuration, not external data.
    """
    
    name: str
    sql: str
    
    async def apply(self, conn: aiosqlite.Connection) -> None:
        """
        Apply migration to database.
        
        Parameters
        ----------
        conn : aiosqlite.Connection
            Database connection.
        """
        await conn.executescript(self.sql)


# Ordered list of all migrations
MIGRATIONS = [
    Migration(
        name="001_initial_schema",
        sql="""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            category TEXT,
            due_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT,
            metadata TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
        CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
        CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
        
        CREATE TABLE IF NOT EXISTS lists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );
        
        CREATE TABLE IF NOT EXISTS list_items (
            id TEXT PRIMARY KEY,
            list_id TEXT NOT NULL,
            content TEXT NOT NULL,
            checked INTEGER NOT NULL DEFAULT 0,
            position INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE
        );
        
        CREATE INDEX IF NOT EXISTS idx_list_items_list_id ON list_items(list_id);
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
    Migration(
        name="003_lists_unified_schema",
        sql="""
        -- Drop old list tables (clean slate as per spec)
        DROP TABLE IF EXISTS list_items;
        DROP TABLE IF EXISTS lists;

        -- Create new unified lists table
        CREATE TABLE IF NOT EXISTS lists (
            name TEXT PRIMARY KEY,
            description TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            metadata TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_lists_created ON lists(created_at);

        -- Create new unified list_items table
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

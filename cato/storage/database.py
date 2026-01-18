"""Async SQLite database wrapper with migration support."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import aiosqlite

from cato.core.exceptions import StorageConnectionError, StorageError
from cato.storage.migrations import MIGRATIONS

logger = logging.getLogger(__name__)


class Database:
    """
    Async SQLite database wrapper.
    
    Provides async connection management, query execution, and automatic
    schema migrations.
    
    Parameters
    ----------
    path : Path
        Path to SQLite database file.
    """
    
    def __init__(self, path: Path) -> None:
        self._path = path
        self._conn: aiosqlite.Connection | None = None
    
    async def connect(self) -> None:
        """
        Open database connection and initialize schema.
        
        Creates database file and parent directories if they don't exist.
        Enables foreign key constraints and runs pending migrations.
        
        Raises
        ------
        StorageConnectionError
            If database connection fails.
        """
        try:
            # Ensure directory exists
            self._path.parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            self._conn = await aiosqlite.connect(self._path)
            self._conn.row_factory = aiosqlite.Row
            
            # Enable foreign keys
            await self._conn.execute("PRAGMA foreign_keys = ON")
            await self._conn.commit()
            
            # Run migrations
            await self._run_migrations()
            
            logger.info(f"Database connected: {self._path}")
            
        except Exception as e:
            raise StorageConnectionError(f"Failed to connect to database: {e}")
    
    async def close(self) -> None:
        """
        Close database connection.
        
        Safe to call multiple times.
        """
        if self._conn:
            await self._conn.close()
            self._conn = None
            logger.info("Database connection closed")
    
    async def execute(self, query: str, params: tuple[Any, ...] = ()) -> aiosqlite.Cursor:
        """
        Execute a write query (INSERT, UPDATE, DELETE).

        Parameters
        ----------
        query : str
            SQL query with ? placeholders.
        params : tuple[Any, ...], optional
            Query parameters.

        Returns
        -------
        aiosqlite.Cursor
            Cursor with lastrowid and rowcount attributes.

        Raises
        ------
        StorageError
            If query execution fails.
        """
        if not self._conn:
            raise StorageError("Database not connected")

        try:
            cursor = await self._conn.execute(query, params)
            await self._conn.commit()
            return cursor
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise StorageError(f"Query execution failed: {e}")
    
    async def fetchone(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> dict[str, Any] | None:
        """
        Fetch a single row from query result.
        
        Parameters
        ----------
        query : str
            SQL SELECT query with ? placeholders.
        params : tuple[Any, ...], optional
            Query parameters.
        
        Returns
        -------
        dict[str, Any] | None
            Row as dictionary if found, None otherwise.
        
        Raises
        ------
        StorageError
            If query execution fails.
        """
        if not self._conn:
            raise StorageError("Database not connected")
        
        try:
            async with self._conn.execute(query, params) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise StorageError(f"Query execution failed: {e}")
    
    async def fetchall(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> list[dict[str, Any]]:
        """
        Fetch all rows from query result.
        
        Parameters
        ----------
        query : str
            SQL SELECT query with ? placeholders.
        params : tuple[Any, ...], optional
            Query parameters.
        
        Returns
        -------
        list[dict[str, Any]]
            List of rows as dictionaries.
        
        Raises
        ------
        StorageError
            If query execution fails.
        """
        if not self._conn:
            raise StorageError("Database not connected")
        
        try:
            async with self._conn.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise StorageError(f"Query execution failed: {e}")
    
    async def _run_migrations(self) -> None:
        """
        Apply pending database migrations.
        
        Creates migrations tracking table if it doesn't exist, then applies
        any migrations that haven't been applied yet.
        """
        if not self._conn:
            return
        
        # Create migrations table
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
                logger.info(f"Applying migration: {migration.name}")
                await migration.apply(self._conn)
                await self._conn.execute(
                    "INSERT INTO migrations (name, applied_at) VALUES (?, ?)",
                    (migration.name, datetime.now().isoformat()),
                )
                await self._conn.commit()
                logger.info(f"Migration applied: {migration.name}")

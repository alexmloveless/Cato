"""Session and thread repository implementation."""

import json
import logging
from datetime import datetime
from typing import Any

from cato.storage.database import Database
from cato.storage.repositories.base import Session, Thread

logger = logging.getLogger(__name__)


class SessionRepository:
    """
    SQLite-backed session repository.
    
    Manages chat sessions and their associated threads.
    
    Parameters
    ----------
    db : Database
        Database connection.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
    
    async def get(self, id: str) -> Session | None:
        """
        Get session by ID.
        
        Parameters
        ----------
        id : str
            Session ID.
        
        Returns
        -------
        Session | None
            Session if found, None otherwise.
        """
        row = await self._db.fetchone("SELECT * FROM sessions WHERE id = ?", (id,))
        return self._row_to_session(row) if row else None
    
    async def get_all(self, limit: int | None = None) -> list[Session]:
        """
        Get all sessions.
        
        Parameters
        ----------
        limit : int | None, optional
            Maximum number of sessions to return.
        
        Returns
        -------
        list[Session]
            List of sessions ordered by start time (newest first).
        """
        query = "SELECT * FROM sessions ORDER BY started_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        rows = await self._db.fetchall(query)
        return [self._row_to_session(row) for row in rows]
    
    async def create(self, session: Session) -> str:
        """
        Create new session.
        
        Parameters
        ----------
        session : Session
            Session to create.
        
        Returns
        -------
        str
            Created session ID.
        """
        await self._db.execute(
            """
            INSERT INTO sessions (id, started_at, ended_at, message_count, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session.id,
                session.started_at.isoformat(),
                session.ended_at.isoformat() if session.ended_at else None,
                session.message_count,
                json.dumps(session.metadata) if session.metadata else None,
            ),
        )
        logger.info(f"Created session: {session.id}")
        return session.id
    
    async def update(self, session: Session) -> None:
        """
        Update existing session.
        
        Parameters
        ----------
        session : Session
            Session to update.
        """
        await self._db.execute(
            """
            UPDATE sessions SET ended_at = ?, message_count = ?, metadata = ?
            WHERE id = ?
            """,
            (
                session.ended_at.isoformat() if session.ended_at else None,
                session.message_count,
                json.dumps(session.metadata) if session.metadata else None,
                session.id,
            ),
        )
        logger.info(f"Updated session: {session.id}")
    
    async def delete(self, id: str) -> None:
        """
        Delete session by ID.
        
        Cascades to all threads due to foreign key constraint.
        
        Parameters
        ----------
        id : str
            Session ID to delete.
        """
        await self._db.execute("DELETE FROM sessions WHERE id = ?", (id,))
        logger.info(f"Deleted session: {id}")
    
    async def get_thread(self, id: str) -> Thread | None:
        """
        Get thread by ID.
        
        Parameters
        ----------
        id : str
            Thread ID.
        
        Returns
        -------
        Thread | None
            Thread if found, None otherwise.
        """
        row = await self._db.fetchone("SELECT * FROM threads WHERE id = ?", (id,))
        return self._row_to_thread(row) if row else None
    
    async def get_threads(self, session_id: str) -> list[Thread]:
        """
        Get all threads for a session.
        
        Parameters
        ----------
        session_id : str
            Session ID.
        
        Returns
        -------
        list[Thread]
            List of threads ordered by creation time.
        """
        rows = await self._db.fetchall(
            "SELECT * FROM threads WHERE session_id = ? ORDER BY created_at ASC",
            (session_id,),
        )
        return [self._row_to_thread(row) for row in rows]
    
    async def create_thread(self, thread: Thread) -> str:
        """
        Create new thread.
        
        Parameters
        ----------
        thread : Thread
            Thread to create.
        
        Returns
        -------
        str
            Created thread ID.
        """
        await self._db.execute(
            """
            INSERT INTO threads (id, session_id, name, created_at, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                thread.id,
                thread.session_id,
                thread.name,
                thread.created_at.isoformat(),
                json.dumps(thread.metadata) if thread.metadata else None,
            ),
        )
        logger.info(f"Created thread: {thread.id}")
        return thread.id
    
    async def update_thread(self, thread: Thread) -> None:
        """
        Update existing thread.
        
        Parameters
        ----------
        thread : Thread
            Thread to update.
        """
        await self._db.execute(
            """
            UPDATE threads SET name = ?, metadata = ?
            WHERE id = ?
            """,
            (
                thread.name,
                json.dumps(thread.metadata) if thread.metadata else None,
                thread.id,
            ),
        )
        logger.info(f"Updated thread: {thread.id}")
    
    async def delete_thread(self, id: str) -> None:
        """
        Delete thread by ID.
        
        Parameters
        ----------
        id : str
            Thread ID to delete.
        """
        await self._db.execute("DELETE FROM threads WHERE id = ?", (id,))
        logger.info(f"Deleted thread: {id}")
    
    def _row_to_session(self, row: dict[str, Any]) -> Session:
        """Convert database row to Session entity."""
        return Session(
            id=row["id"],
            started_at=datetime.fromisoformat(row["started_at"]),
            ended_at=datetime.fromisoformat(row["ended_at"]) if row["ended_at"] else None,
            message_count=row["message_count"],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )
    
    def _row_to_thread(self, row: dict[str, Any]) -> Thread:
        """Convert database row to Thread entity."""
        return Thread(
            id=row["id"],
            session_id=row["session_id"],
            name=row["name"],
            created_at=datetime.fromisoformat(row["created_at"]),
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
        )

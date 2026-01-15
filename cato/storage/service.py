"""Unified storage service providing access to all repositories."""

import logging
from pathlib import Path

from cato.core.config import CatoConfig
from cato.storage.database import Database
from cato.storage.repositories import (
    ListItemRepository,
    ListRepository,
    SessionRepository,
    TaskRepository,
)

logger = logging.getLogger(__name__)


class Storage:
    """
    Unified storage service.
    
    Provides access to all repositories through a single interface.
    Manages database connection lifecycle.
    
    Parameters
    ----------
    db : Database
        Database connection.
    
    Attributes
    ----------
    tasks : TaskRepository
        Task repository.
    lists : ListRepository
        List repository.
    list_items : ListItemRepository
        List item repository.
    sessions : SessionRepository
        Session repository.
    """
    
    def __init__(self, db: Database) -> None:
        self._db = db
        self.tasks = TaskRepository(db)
        self.lists = ListRepository(db)
        self.list_items = ListItemRepository(db)
        self.sessions = SessionRepository(db)
    
    async def connect(self) -> None:
        """
        Connect to database and run migrations.
        
        Must be called before using any repositories.
        """
        await self._db.connect()
        logger.info("Storage service connected")
    
    async def close(self) -> None:
        """
        Close database connection.
        
        Should be called during application shutdown.
        """
        await self._db.close()
        logger.info("Storage service closed")


async def create_storage(config: CatoConfig) -> Storage:
    """
    Create and connect storage service.
    
    Factory function that creates a Storage instance with the configured
    database path and establishes connection with migrations.
    
    Parameters
    ----------
    config : CatoConfig
        Application configuration containing storage settings.
    
    Returns
    -------
    Storage
        Connected storage service ready for use.
    
    Raises
    ------
    StorageConnectionError
        If database connection fails.
    
    Examples
    --------
    >>> config = load_config()
    >>> storage = await create_storage(config)
    >>> task = await storage.tasks.get("task_id")
    >>> await storage.close()
    """
    db_path = Path(config.storage.database_path)
    db = Database(db_path)
    storage = Storage(db)
    await storage.connect()
    logger.info(f"Storage created with database at: {db_path}")
    return storage

"""Base repository protocol and entity models."""

import json
import uuid
from datetime import datetime
from typing import Any, Literal, Protocol, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Repository(Protocol[T]):
    """
    Generic repository protocol for CRUD operations.
    
    Type parameter T represents the entity type managed by the repository.
    """
    
    async def get(self, id: str) -> T | None:
        """
        Get entity by ID.
        
        Parameters
        ----------
        id : str
            Entity ID.
        
        Returns
        -------
        T | None
            Entity if found, None otherwise.
        """
        ...
    
    async def get_all(self, **filters: Any) -> list[T]:
        """
        Get all entities, optionally filtered.
        
        Parameters
        ----------
        **filters
            Optional filter parameters.
        
        Returns
        -------
        list[T]
            List of matching entities.
        """
        ...
    
    async def create(self, entity: T) -> str:
        """
        Create entity.
        
        Parameters
        ----------
        entity : T
            Entity to create.
        
        Returns
        -------
        str
            ID of created entity.
        """
        ...
    
    async def update(self, entity: T) -> None:
        """
        Update existing entity.
        
        Parameters
        ----------
        entity : T
            Entity to update.
        """
        ...
    
    async def delete(self, id: str) -> None:
        """
        Delete entity by ID.
        
        Parameters
        ----------
        id : str
            Entity ID to delete.
        """
        ...


# Entity models
class Task(BaseModel):
    """
    Task entity.
    
    Parameters
    ----------
    id : str
        Unique task identifier.
    title : str
        Task title.
    description : str | None
        Optional task description.
    status : Literal["active", "in_progress", "completed", "deleted"]
        Task status.
    priority : Literal["low", "medium", "high", "urgent"]
        Task priority level.
    category : str | None
        Optional category for grouping.
    due_date : datetime | None
        Optional due date.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    completed_at : datetime | None
        Completion timestamp if completed.
    metadata : dict[str, Any]
        Extensible metadata field.
    """
    
    id: str
    title: str
    description: str | None = None
    status: Literal["active", "in_progress", "completed", "deleted"] = "active"
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    category: str | None = None
    due_date: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# List and ListItem models moved to cato.core.types for unified list system


class Session(BaseModel):
    """
    Session entity for chat tracking.
    
    Parameters
    ----------
    id : str
        Unique session identifier.
    started_at : datetime
        Session start timestamp.
    ended_at : datetime | None
        Session end timestamp if ended.
    message_count : int
        Number of messages in session.
    metadata : dict[str, Any]
        Extensible metadata field.
    """
    
    id: str
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: datetime | None = None
    message_count: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class Thread(BaseModel):
    """
    Thread entity for conversation continuation.
    
    Parameters
    ----------
    id : str
        Unique thread identifier.
    session_id : str
        Parent session ID.
    name : str | None
        Optional thread name.
    created_at : datetime
        Creation timestamp.
    metadata : dict[str, Any]
        Extensible metadata field.
    """
    
    id: str
    session_id: str
    name: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: dict[str, Any] = Field(default_factory=dict)


def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID for entities.
    
    Parameters
    ----------
    prefix : str, optional
        Optional prefix for the ID.
    
    Returns
    -------
    str
        Unique ID string.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = uuid.uuid4().hex[:8]
    
    if prefix:
        return f"{prefix}_{timestamp}_{unique}"
    return f"{timestamp}_{unique}"

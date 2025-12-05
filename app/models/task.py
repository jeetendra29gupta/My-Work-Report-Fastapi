from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app.utilities.helper import get_utc_now


class TaskStatus(str, Enum):
    PENDING = "Pending"
    OPEN = "Open"
    CLOSED = "Closed"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    note: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.OPEN, index=True)

    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(
        default_factory=get_utc_now, alias="created_at", index=True
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now, alias="updated_at", index=True
    )

    owner_id: int = Field(foreign_key="users.id", index=True)
    owner: Optional["User"] = Relationship()  # noqa

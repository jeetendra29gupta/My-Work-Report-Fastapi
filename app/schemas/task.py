from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from app.models.task import TaskStatus
from app.schemas.user import ReadUser


class CreateTask(SQLModel):
    title: str
    description: Optional[str] = None
    note: Optional[str] = None


class UpdateTask(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    note: Optional[str] = None


class ReadTask(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    note: Optional[str] = None
    status: TaskStatus
    owner: ReadUser
    created_at: datetime
    updated_at: datetime

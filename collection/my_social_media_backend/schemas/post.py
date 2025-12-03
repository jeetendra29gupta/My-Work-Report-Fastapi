from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..schemas.user import UserRead


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author: UserRead

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship
from sqlmodel import SQLModel

from ..utilities.database import engine


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    is_published: bool = False

    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    # Relationship back to user and foreign key to user
    user_id: int = Field(default=None, foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="posts")  # noqa


def init_post_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import Field, Relationship
from sqlmodel import SQLModel

from ..utilities.database import engine


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email_id: EmailStr = Field(unique=True)
    phone_no: str
    hashed_password: str
    role: UserRole = UserRole.USER

    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    # Relationship: One user -> many posts
    posts: List["Post"] = Relationship(back_populates="author")  # noqa


def init_user_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

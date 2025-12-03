from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import SQLModel

from ..utilities.database import engine


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPPORT = "support"


class Auth(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email_id: EmailStr = Field(unique=True)
    phone_no: str
    hashed_password: str
    role: UserRole = UserRole.USER

    is_active: bool = True
    created_at: datetime
    updated_at: datetime


def init_auth_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

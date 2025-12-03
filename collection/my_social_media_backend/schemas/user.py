from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from ..models.user import UserRole


class UserCreate(BaseModel):
    full_name: str
    email_id: EmailStr
    phone_no: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_no: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserRoleChange(BaseModel):
    role: UserRole


class UserRead(BaseModel):
    id: int
    full_name: str
    email_id: EmailStr
    phone_no: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

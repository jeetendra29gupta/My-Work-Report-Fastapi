from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UpdateUser(BaseModel):
    full_name: Optional[str] = None
    phone_no: Optional[str] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class RoleChange(BaseModel):
    role: UserRole


class ReadUser(BaseModel):
    id: int
    full_name: str
    email_id: EmailStr
    phone_no: Optional[str] = None
    role: UserRole
    created_at: datetime
    updated_at: datetime

class UserSuccessMessage(BaseModel):
    status_code: int
    detail: dict[str, Any]
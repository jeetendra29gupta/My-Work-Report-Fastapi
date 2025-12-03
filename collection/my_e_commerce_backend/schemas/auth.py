from datetime import datetime

from pydantic import BaseModel, EmailStr

from ..models.auth import UserRole


class AuthSignup(BaseModel):
    full_name: str
    email_id: EmailStr
    phone_no: str
    password: str


class AuthUser(BaseModel):
    id: int
    full_name: str
    email_id: EmailStr
    phone_no: str
    role: UserRole
    created_at: datetime
    updated_at: datetime


class AuthToken(BaseModel):
    access_token: str
    token_type: str

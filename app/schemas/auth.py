from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    full_name: str = Field(..., min_length=8, max_length=120)
    email_id: EmailStr
    phone_no: Optional[str] = Field(None, min_length=8, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email_id: EmailStr
    password: str = Field(..., min_length=8)


class UserToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class Role(str, Enum):
    candidate = "candidate"
    recruiter = "recruiter"
    admin = "admin"


class RegisterRequest(BaseModel):
    email: str = Field(pattern=EMAIL_PATTERN)
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1)
    # admins are never self-registered; they are created by a seed script
    role: Literal["candidate", "recruiter"]


class LoginRequest(BaseModel):
    email: str = Field(pattern=EMAIL_PATTERN)
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Seconds until the token expires")


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime
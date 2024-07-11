from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str
    role: str
    created_at: Optional[datetime] = None


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    updated_at: Optional[datetime] = None

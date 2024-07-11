from sqlmodel import SQLModel, create_engine, Field, Session
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
from enum import Enum
import os

load_dotenv()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(index=True)


DATABASE_URL_1: str = os.getenv("DATABASE_URL_1")
engine = create_engine(DATABASE_URL_1)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

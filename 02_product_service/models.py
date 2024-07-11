from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


# Product


class ProductAdd(SQLModel):
    name: str
    description: str
    price: float
    category_id: int
    available: bool
    created_at: datetime
    updated_at: datetime


class ProductUpdate(SQLModel):
    name: str = None
    description: str = None
    price: float = None
    category_id: int = None
    available: bool = None
    updated_at: Optional[datetime] = datetime.utcnow()


# Category


class CategoryAdd(SQLModel):
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class CategoryUpdate(SQLModel):
    name: str = None
    description: str = None
    updated_at: Optional[datetime] = datetime.utcnow()


# Review


class ReviewAdd(SQLModel):
    review_text: str
    product_id: int
    created_at: datetime
    updated_at: datetime


class ReviewUpdate(SQLModel):
    review_text: str = None
    updated_at: Optional[datetime] = datetime.utcnow()


# Rating


class RatingAdd(SQLModel):
    rating: int
    product_id: int
    created_at: datetime
    updated_at: datetime


class RatingUpdate(SQLModel):
    rating: int = None
    updated_at: Optional[datetime] = datetime.utcnow()

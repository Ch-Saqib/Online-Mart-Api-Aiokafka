from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from typing import Optional, Annotated, List
from datetime import datetime
import os

load_dotenv()

conn_str = os.getenv("DATABASE_URL_2")
engine = create_engine(conn_str)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    product_category: "Product" = Relationship(back_populates="category")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: "Category" = Relationship(back_populates="product_category")
    reviews: list["Review"] = Relationship(back_populates="product_review")
    ratings: list["Rating"] = Relationship(back_populates="product_rating")


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    review_text: str
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    created_at: Optional[datetime] = None
    product_review: "Product" = Relationship(back_populates="reviews")


class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    created_at: Optional[datetime] = None
    product_rating: "Product" = Relationship(back_populates="ratings")


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

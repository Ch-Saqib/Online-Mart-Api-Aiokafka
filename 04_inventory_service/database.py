from sqlmodel import Field, SQLModel, create_engine, Session, Relationship
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv()


# Inventory model
class Inventory(SQLModel, table=True):
    inventory_id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int]  # This will reference a product ID from the Product service
    quantity: Optional[int]
    location_id: Optional[int] = Field(default=None, foreign_key="location.location_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    location: Optional["Location"] = Relationship(back_populates="inventory_items")
    # stock_movements: List["StockMovement"] = Relationship(back_populates="inventory")


# Location model
class Location(SQLModel, table=True):
    location_id: Optional[int] = Field(default=None, primary_key=True)
    location_name: str
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    inventory_items: List[Inventory] = Relationship(back_populates="location")

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL_4")
engine = create_engine(DATABASE_URL)


# Create tables
def create_tables():
    SQLModel.metadata.create_all(engine)


# Example of adding an inventory record
def get_session():
    with Session(engine) as session:
        yield session

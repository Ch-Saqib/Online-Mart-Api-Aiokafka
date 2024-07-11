from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


class Order(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # This ID will be managed and validated by the User Management service
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: str
    total_amount: float

    order_items: List["OrderItem"] = Relationship(back_populates="order_item")
    shipment: Optional["Shipment"] = Relationship(back_populates="order_shipment")


class OrderItem(SQLModel, table=True):
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    product_id: int  # Assume this is managed and validated by the Product service
    quantity: int
    price: float
    total_price: float

    order_item: Order = Relationship(back_populates="order_items")


class Shipment(SQLModel, table=True):
    shipment_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    shipment_date: datetime = Field(default_factory=datetime.utcnow)
    delivery_date: Optional[datetime] = None
    status: str

    order_shipment: Order = Relationship(back_populates="shipment")


# Database url
DATABASE_URL = os.getenv("DATABASE_URL_3")
# Create Engine
engine = create_engine(DATABASE_URL)


# Create Tables
def create_tables():
    SQLModel.metadata.create_all(engine)


# Get Session / Interaction With Database
def get_session():
    with Session(engine) as session:
        yield session

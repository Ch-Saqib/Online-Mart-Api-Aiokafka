from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


# Order Models
class OrderAdd(SQLModel):
    user_id: int
    order_date: Optional[datetime] = None
    status: str
    total_amount: float


class OrderUpdate(SQLModel):
    status: str = None
    total_amount: float = None


# OrderItem Models
class OrderItemAdd(SQLModel):
    order_id: int
    product_id: int
    quantity: int
    price: float
    total_price: float


class OrderItemUpdate(SQLModel):
    quantity: int = None
    price: float = None
    total_price: float = None


# Shipment Models
class ShipmentAdd(SQLModel):
    order_id: int
    shipment_date: Optional[datetime]
    delivery_date: Optional[datetime] = None
    status: str


class ShipmentUpdate(SQLModel):
    shipment_date: Optional[datetime] = datetime.utcnow()
    delivery_date: Optional[datetime] = datetime.utcnow()
    status: str = None

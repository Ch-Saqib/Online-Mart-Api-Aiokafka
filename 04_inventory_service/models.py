from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class InventoryAdd(SQLModel):
    location_id: Optional[int]
    product_id: Optional[int]
    quantity: int
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()


class InventoryUpdate(SQLModel):
    product_id: Optional[int] = None
    quantity: int = None
    location_id: Optional[int] = None
    updated_at: Optional[datetime] = datetime.utcnow()


# Location model


class LocationAdd(SQLModel):
    location_name: str
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LocationUpdate(SQLModel):
    location_name: str = None
    address: Optional[str] = None
    updated_at: Optional[datetime] = datetime.utcnow()




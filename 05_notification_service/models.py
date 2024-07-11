from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel


class NotificationAdd(SQLModel):
    user_id: int
    order_id: int
    message: str
    read: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class NotificationUpdate(SQLModel):
    read: bool = None
    updated_at: Optional[datetime] = datetime.utcnow()

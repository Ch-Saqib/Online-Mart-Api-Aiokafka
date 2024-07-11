from aiokafka import AIOKafkaProducer
from fastapi import Depends, APIRouter
from services.notification_service import *
from models import *
from database import *
from contextlib import asynccontextmanager
from typing import Annotated
import notification_pb2
from datetime import datetime
from services.consumers import *

notification_router = APIRouter()


# Crud Notification
@notification_router.get("/notification")
def get_notification(session: Annotated[Session, Depends(get_session)]):
    return get_notifications(session=session)


@notification_router.get("/notification/{notification_id}")
def get_notification_by_id(
    notification_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_notification_id(notification_id=notification_id, session=session)


@notification_router.post("/add_notification")
async def create_notification(notification_add: NotificationAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def dt_to_isoformat(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = dt_to_isoformat(notification_add.created_at)
        updated_at_str = dt_to_isoformat(notification_add.updated_at)

        add_data = notification_pb2.Notification_Proto(
            user_id=notification_add.user_id,
            order_id=notification_add.order_id,
            message=notification_add.message,
            read=notification_add.read,
            created_at=created_at_str,
            updated_at=updated_at_str,
        )
        protoc_data = add_data.SerializeToString()
        print(f"Serialized Data : ", protoc_data)
        # Produce message
        await producer.send_and_wait("notification_service", protoc_data)
        return notification_add
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@notification_router.put("/update_notification/{notification_id}")
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_notifications(
        notification_id=notification_id,
        notification_update=notification_update,
        session=session,
    )


@notification_router.delete("/delete_notification/{notification_id}")
def delete_notification(
    notification_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_notifications(notification_id=notification_id, session=session)

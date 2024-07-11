from database import *
from models import *
from fastapi import HTTPException
import notification_pb2


def get_notifications(session: Session):
    try:
        get_data = session.exec(select(Notification)).all()
        return get_data
    except Exception as e:
        print(e)


def get_notification_id(notification_id: int, session: Session):
    try:
        get_data = session.get(Notification, notification_id)
        return get_data
    except Exception as e:
        print(e)


async def add_notification(
    notification_add: notification_pb2.Notification_Proto, session: Session
):
    try:
        db_add = Notification(
            user_id=notification_add.user_id,
            order_id=notification_add.order_id,
            message=notification_add.message,
            read=notification_add.read,
            created_at=notification_add.created_at,
            updated_at=notification_add.updated_at,
        )
        session.add(db_add)
        session.commit()
        session.refresh(db_add)
        return db_add
    except Exception as e:
        print(e)


def update_notifications(
    notification_id: int, notification_update: NotificationUpdate, session: Session
):
    try:
        db_notification = session.get(Notification, notification_id)
        if db_notification is None:
            raise HTTPException(404, "Notification not found")
        notification_data = notification_update.model_dump(exclude_unset=True)
        db_notification.sqlmodel_update(notification_data)
        session.add(db_notification)
        session.commit()
        session.refresh(db_notification)
        return db_notification
    except Exception as e:
        print(e)


def delete_notifications(notification_id: int, session: Session):
    try:
        db_notification = session.get(Notification, notification_id)
        if db_notification is None:
            raise HTTPException(404, "Notification not found")
        session.delete(db_notification)
        session.commit()
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        print(e)

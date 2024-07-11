from aiokafka import AIOKafkaProducer
from fastapi import Depends, APIRouter
from datetime import datetime
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Annotated
from services.order_service import *
from services.consumers import *
from services.notification_consumer import *
from database import *
import order_pb2


order_router = APIRouter()
orderitem_router = APIRouter()
shipment_router = APIRouter()


# Crud Order
@order_router.get("/orders")
def get_all_orders(session: Annotated[Session, Depends(get_session)]):
    return get_orders(session=session)


@order_router.get("/order/{order_id}")
def get_order_by_id(order_id: int, session: Annotated[Session, Depends(get_session)]):
    return get_order_id(order_id=order_id, session=session)


@order_router.post("/order_add")
async def add_order(order: OrderAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        order_at_str = datetime_to_iso(order.order_date)

        add_order = order_pb2.Order_Proto(
            user_id=order.user_id,
            order_date=order_at_str,
            status=order.status,
            total_amount=order.total_amount,
        )
        protoc_data = add_order.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")
        # Produce message
        await producer.send_and_wait("order_service", protoc_data)
        return order
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@order_router.put("/order_update/{order_id}")
def update_order_by_id(
    order_id: int,
    order_update: OrderUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_order(order_id=order_id, order_update=order_update, session=session)


@order_router.delete("/order_delete/{order_id}")
def delete_order_by_id(
    order_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_order_id(order_id=order_id, session=session)


# Crud OrderItems
@orderitem_router.get("/order_items")
def get_all_order_items(session: Annotated[Session, Depends(get_session)]):
    return get_order_items(session=session)


@orderitem_router.get("/order_item/{order_item_id}")
def get_order_item_by_id(
    order_item_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_order_item_id(order_item_id=order_item_id, session=session)


@orderitem_router.post("/order_item_add")
async def add_order_item(order_item: OrderItemAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        add_order_items = order_pb2.OrderItem_Proto(
            order_id=order_item.order_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
            price=order_item.price,
            total_price=order_item.total_price,
        )
        protoc_data = add_order_items.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")
        # Produce message
        await producer.send_and_wait("order_items_service", protoc_data)
        return order_item
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@orderitem_router.put("/order_item_update/{order_item_id}")
def update_order_item_by_id(
    order_item_id: int,
    order_item_update: OrderItemUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_order_item(
        order_item_id=order_item_id,
        order_item_update=order_item_update,
        session=session,
    )


@orderitem_router.delete("/order_item_delete/{order_item_id}")
def delete_order_item_by_id(
    order_item_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_order_item_id(order_item_id=order_item_id, session=session)


# Crud Shipment
@shipment_router.get("/shipments")
def get_all_shipments(session: Annotated[Session, Depends(get_session)]):
    return get_shipments(session=session)


@shipment_router.get("/shipment/{shipment_id}")
def get_shipment_by_id(
    shipment_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_shipment_id(shipment_id=shipment_id, session=session)


@shipment_router.post("/shipment_add")
async def add_shipment(
    shipment: ShipmentAdd, session: Annotated[Session, Depends(get_session)]
):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        shipment_date_at_str = datetime_to_iso(shipment.shipment_date)
        delivery_date_at_str = datetime_to_iso(shipment.delivery_date)

        add_shipment = order_pb2.Shipment_Proto(
            order_id=shipment.order_id,
            shipment_date=shipment_date_at_str,
            delivery_date=delivery_date_at_str,
            status=shipment.status,
        )
        protoc_data = add_shipment.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")
        # Produce message
        await producer.send_and_wait("shipment_service", protoc_data)
        return shipment
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@shipment_router.put("/shipment_update/{shipment_id}")
def update_shipment_by_id(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_shipment(
        shipment_id=shipment_id, shipment_update=shipment_update, session=session
    )


@shipment_router.delete("/shipment_delete/{shipment_id}")
def delete_shipment_by_id(
    shipment_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_shipment_id(shipment_id=shipment_id, session=session)

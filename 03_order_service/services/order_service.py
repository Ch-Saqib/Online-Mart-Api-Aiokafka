from models import *
from database import *
from fastapi import HTTPException
import order_pb2


# Crud Order
def get_orders(session: Session):
    try:
        orders = session.exec(select(Order)).all()
        return orders
    except Exception as error:
        print(error)


def get_order_id(order_id: int, session: Session):
    try:
        order = session.get(Order, order_id)
        if order is None:
            raise HTTPException(404, "Order not found")
        return order
    except Exception as error:
        print(error)


async def create_order(order: order_pb2.Order_Proto, session: Session):
    try:
        db_order = Order(
            user_id=order.user_id,
            order_date=order.order_date,
            status=order.status,
            total_amount=order.total_amount,
        )
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def update_order(order_id: int, order_update: OrderUpdate, session: Session):
    try:
        db_order = session.get(Order, order_id)
        if db_order is None:
            raise HTTPException(404, "Order not found")
        order_data = order_update.model_dump(exclude_unset=True)
        db_order.sqlmodel_update(order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def delete_order_id(order_id: int, session: Session):
    try:
        order = session.get(Order, order_id)
        if order is None:
            raise HTTPException(404, "Order not found")
        session.delete(order)
        session.commit()
        return {"message": "Order Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


# Crud OrderItems
def get_order_items(session: Session):
    try:
        order_items = session.exec(select(OrderItem)).all()
        if order_items is None:
            raise HTTPException(404, "No order items found")
        return order_items
    except Exception as error:
        print(error)


def get_order_item_id(order_item_id: int, session: Session):
    try:
        order_item = session.get(OrderItem, order_item_id)
        if order_item is None:
            raise HTTPException(404, "Order item not found")
        return order_item
    except Exception as error:
        print(error)


async def create_order_item(order_item: order_pb2.OrderItem_Proto, session: Session):
    try:
        validate_order_id = session.get(Order, order_item.order_id)
        if validate_order_id is None:
            raise HTTPException(404, "Order not found")

        db_order_item = OrderItem(
            order_id=order_item.order_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
            price=order_item.price,
            total_price=order_item.total_price,
        )
        session.add(db_order_item)
        session.commit()
        session.refresh(db_order_item)
        return db_order_item
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def update_order_item(
    order_item_id: int, order_item_update: OrderItemUpdate, session: Session
):
    try:
        db_order_item = session.get(OrderItem, order_item_id)
        if db_order_item is None:
            raise HTTPException(404, "Order item not found")
        order_item_data = order_item_update.model_dump(exclude_unset=True)
        db_order_item.sqlmodel_update(order_item_data)
        session.add(db_order_item)
        session.commit()
        session.refresh(db_order_item)
        return db_order_item
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def delete_order_item_id(order_item_id: int, session: Session):
    try:
        order_item = session.get(OrderItem, order_item_id)
        if order_item is None:
            raise HTTPException(404, "Order item not found")
        session.delete(order_item)
        session.commit()
        return {"message": "Order item Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


# Crud Shipment
def get_shipments(session: Session):
    try:
        shipments = session.exec(select(Shipment)).all()
        if shipments is None:
            raise HTTPException(404, "No shipments found")
        return shipments
    except Exception as error:
        print(error)


def get_shipment_id(shipment_id: int, session: Session):
    try:
        shipment = session.get(Shipment, shipment_id)
        if shipment is None:
            raise HTTPException(404, "Shipment not found")
        return shipment
    except Exception as error:
        print(error)


async def create_shipment(shipment: order_pb2.Shipment_Proto, session: Session):
    try:
        validate_order_id = session.get(Order, shipment.order_id)
        if validate_order_id is None:
            raise HTTPException(404, "Order not found")
        db_shipment = Shipment(
            order_id=shipment.order_id,
            shipment_date=shipment.shipment_date,
            delivery_date=shipment.delivery_date,
            status=shipment.status,
        )
        session.add(db_shipment)
        session.commit()
        session.refresh(db_shipment)
        return db_shipment
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def update_shipment(
    shipment_id: int, shipment_update: ShipmentUpdate, session: Session
):
    try:
        db_shipment = session.get(Shipment, shipment_id)
        if db_shipment is None:
            raise HTTPException(404, "Shipment not found")
        shipment_data = shipment_update.model_dump(exclude_unset=True)
        db_shipment.sqlmodel_update(shipment_data)
        session.add(db_shipment)
        session.commit()
        session.refresh(db_shipment)
        return db_shipment
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def delete_shipment_id(shipment_id: int, session: Session):
    try:
        shipment = session.get(Shipment, shipment_id)
        if shipment is None:
            raise HTTPException(404, "Shipment not found")
        session.delete(shipment)
        session.commit()
        return {"message": "Shipment Deleted Successfully"}
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")


def validate_by_id(order_id: int, session: Session):
    try:
        order = session.get(Order, id)
        if order is None:
            raise HTTPException(404, "Order not found")
        return order
    except Exception as error:
        print(error)
        raise HTTPException(400, "Something went wrong")

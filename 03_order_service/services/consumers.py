from aiokafka import AIOKafkaConsumer
from database import get_session
from services.order_service import *
import order_pb2
import logging

logging.basicConfig(level=logging.INFO)


# Order Consumer
async def consume_order(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers, group_id="order_group"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: %s ", msg.value)
            order = order_pb2.Order_Proto()
            order.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", order)

            with next(get_session()) as session:
                try:
                    result = await create_order(order=order, session=session)
                    logger.info("Order added: %s", result)
                except Exception as e:
                    logger.error("Error adding order: %s", e)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


# Order_Items Consumer
async def consume_orderitems(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers, group_id="orderitem_group"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: ", msg.value)
            order_item = order_pb2.OrderItem_Proto()
            order_item.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", order_item)

            with next(get_session()) as session:
                try:
                    result = await create_order_item(
                        order_item=order_item, session=session
                    )
                    logger.info("Order Item added: %s", result)
                except Exception as e:
                    logger.error("Error adding order item: %s", e)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


# Shipment Consumer
async def consume_shipments(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers, group_id="shipment_group"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: ", msg.value)
            shipment = order_pb2.Shipment_Proto()
            shipment.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", shipment)

            with next(get_session()) as session:
                try:
                    result = await create_shipment(shipment=shipment, session=session)
                    logger.info("Shipment added: %s", result)
                except Exception as e:
                    logger.error("Error adding shipment: %s", e)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

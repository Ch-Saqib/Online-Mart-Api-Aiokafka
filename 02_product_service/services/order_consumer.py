from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from services.product_service import *
from database import get_session
import order_pb2
import logging

logging.basicConfig(level=logging.INFO)


# Order Consumer
async def consume_orderitem(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic, bootstrap_servers=bootstrap_servers, group_id="orderitem_group"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: %s ", msg.value)
            orderitem = order_pb2.OrderItem_Proto()
            orderitem.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", orderitem)

            # Get ID
            product_id = orderitem.product_id
            logger.info("PRODUCT ID: %s", product_id)

            with next(get_session()) as session:
                try:
                    # Get OrderItem
                    orderitem = validate_product_id(
                        product_id=product_id, session=session
                    )
                    logger.info("ORDER VALIDATION CHECK %s", orderitem)
                    if orderitem is None:
                        logger.info("PRODUCT VALIDATION CHECK NOT NONE")
                    # Producer Use For Send MSG in Inventory Topic
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("order_service", msg.value)
                    finally:
                        await producer.stop()
                except ValueError as e:
                    logger.error("Invalid order ID: %s", str(e))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

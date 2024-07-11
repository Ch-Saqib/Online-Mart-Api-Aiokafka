from aiokafka import AIOKafkaConsumer
from services.notification_service import *
import logging
import notification_pb2
from database import *

logging.basicConfig(level=logging.INFO)


async def consume_notification(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="notification_group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: %s", msg.value)
            notification_add = notification_pb2.Notification_Proto()
            notification_add.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", notification_add)

            # order_id = notification_add.order_id
            # logger.info("Order ID: %s", order_id)

            with next(get_session()) as session:
                try:
                    result = await add_notification(
                        notification_add=notification_add, session=session
                    )
                    logger.info("Order added: %s", result)
                    return result
                except Exception as e:
                    logger.error("Error: %s", e)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

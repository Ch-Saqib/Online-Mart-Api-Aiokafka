from aiokafka import AIOKafkaConsumer
import inventory_pb2
from database import *
from services.inventory_service import add_inventory
import logging

logging.basicConfig(level=logging.INFO)


async def consume_inventory(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory_group",
        # auto_offset_reset="earliest",
        enable_auto_commit=False,
        session_timeout_ms=30000,
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("Consumed message: %s", msg.value)
            inventory = inventory_pb2.Inventory_Proto()
            inventory.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", inventory)
            # Access product_id using dot notation
            productid = inventory.product_id

            logger.info("ُPRODUCT ID:  %s ", productid)
            with next(get_session()) as session:
                try:
                    result = await add_inventory(inventory=inventory, session=session)
                    logger.info("Location added: %s", result)
                    return result
                except Exception as e:
                    logger.error("Error adding location: %s", e)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

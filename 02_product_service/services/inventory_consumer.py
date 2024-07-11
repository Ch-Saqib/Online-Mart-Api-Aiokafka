from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import inventory_pb2
from database import *
import logging
from services.product_service import validate_product_id

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

            # Checking Product Id
            with next(get_session()) as session:
                try:
                    product = validate_product_id(product_id=productid, session=session)
                    logger.info("PRODUCT VALIDATION CHECK %s", product)

                    if product is None:
                        logger.info("PRODUCT VALIDATION CHECK NOT NONE")
                    # Producer Use For Send MSG in Inventory Topic
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("inventory_service", msg.value)
                    finally:
                        await producer.stop()

                except ValueError as e:
                    logger.error("Invalid product ID: %s", str(e))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

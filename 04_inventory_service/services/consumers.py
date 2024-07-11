from aiokafka import AIOKafkaConsumer
import inventory_pb2
from services.inventory_service import add_location
from database import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level as needed


async def consume_location(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="location_group",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logger.info("Consumed message: %s", msg.value)
            location = inventory_pb2.Location_Proto()
            location.ParseFromString(msg.value)
            logger.debug("Deserialized Data: %s", location)

            with next(get_session()) as session:
                try:
                    result = await add_location(location=location, session=session)
                    logger.info("Location added: %s", result)
                    return result
                except Exception as e:
                    logger.error("Error adding location: %s", e)
    finally:
        await consumer.stop()

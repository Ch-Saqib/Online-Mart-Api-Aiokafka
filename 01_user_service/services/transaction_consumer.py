from aiokafka import AIOKafkaConsumer
from services.user_service import *
from database import *
import logging
import payment_pb2
from aiokafka import AIOKafkaProducer

logging.basicConfig(level=logging.INFO)


async def consume_transaction(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="transaction_group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            logger.info("consumed: %s", msg.value)
            payment_request = payment_pb2.Transaction_Proto()
            payment_request.ParseFromString(msg.value)

            logger.debug("Decrialized Transaction : %s", payment_request)
            print("Decrialized Data", payment_request)

            user_id = payment_request.user_id
            print("user_id", user_id)
            with next(get_session()) as session:
                try:
                    validate_id = validate_by_id(user_id=user_id, session=session)
                    if validate_id is None:
                        logger.info("User not found")
                    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
                    await producer.start()
                    try:
                        await producer.send_and_wait("transaction_service", msg.value)
                    finally:
                        await producer.stop()

                except Exception as e:
                    logger.error("Error adding transaction to database: %s", e)

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

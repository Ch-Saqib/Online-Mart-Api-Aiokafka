from aiokafka import AIOKafkaConsumer
import product_pb2
from database import get_session
from services.product_service import *
import logging


logging.basicConfig(level=logging.INFO)


# Product Consumer
async def consume_product(topic: str, bootstrap_servers: str):
    logger = logging.getLogger(__name__)
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product_group",
        # auto_offset_reset="earliest",
        enable_auto_commit=False,
        session_timeout_ms=30000,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logger.info("consumed: %s", msg.value)
            product = product_pb2.Product_Proto()
            product.ParseFromString(msg.value)
            logger.debug("Deserialized: %s", product)

            with next(get_session()) as session:
                result = await add_product(product=product, session=session)
                # print(f"Product insertion result: {result}")
                return result

    finally:
        await consumer.stop()


# Category consumed
async def consume_category(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="category_group",
        # auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print("consumed: ", msg.value)
            category = product_pb2.Category_Proto()
            category.ParseFromString(msg.value)
            # print("Deserialized: ", category)

            with next(get_session()) as session:
                result = await add_category(category=category, session=session)
                # print(f"Category insertion result: {result}")
                return result

    finally:
        await consumer.stop()


# Review Consumed
async def consume_review(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="review_group",
        # auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print("consumed: ", msg.value)
            review = product_pb2.Review_Proto()
            review.ParseFromString(msg.value)
            # print("Deserialized: ", review)

            with next(get_session()) as session:
                result = await add_review(review=review, session=session)
                # print(f"Review insertion result: {result}")
                return result

    finally:
        await consumer.stop()


# Rating Consumed
async def consume_rating(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="rating_group",
        # auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # print("consumed: ", msg.value)
            rating = product_pb2.Rating_Proto()
            rating.ParseFromString(msg.value)
            # print("Deserialized: ", rating)

            with next(get_session()) as session:
                result = await add_rating(rating=rating, session=session)
                # print(f"Rating insertion result: {result}")
                return result

    finally:
        await consumer.stop()

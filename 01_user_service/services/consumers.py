from aiokafka import AIOKafkaConsumer
import user_pb2
from fastapi import HTTPException
from services.user_service import create_user
from sqlmodel import Session
from database import engine


async def consume(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="user_group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            # print("consumed: ", msg.value)
            user = user_pb2.User_Proto()
            user.ParseFromString(msg.value)
            # print(f"Decrialized Data : {user}")

            with Session(bind=engine) as session:
                result = await create_user(user=user, session=session)
                if not result:
                    raise HTTPException(status_code=400, detail="User creation failed")

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

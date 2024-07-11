import json
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Field, create_engine, SQLModel, Session, select
from main import get_session, app, User, UserCreate
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
import asyncio
# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Create a new engine instance for the test database
engine = create_engine(TEST_DATABASE_URL, echo=True)


# Create a session local fixture to ensure a clean session for each test
def session_local():
    with Session(engine) as session:
        yield session


# Override get_session dependency in tests with the session_local fixture
app.dependency_overrides[get_session] = session_local

# Create a TestClient instance with the overridden dependency
client = TestClient(app)


# Create the test database and tables
@pytest.fixture(scope="module", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


# Test Cases:
@pytest.mark.asyncio
async def test_signup():
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    consumer = AIOKafkaConsumer(
        "user_service", bootstrap_servers="broker:19092", group_id="user_group"
    )

    await retry_connection(producer.start)
    await retry_connection(consumer.start)

    try:
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123",
            "role": "user",
            "created_at": "2024-07-08T12:00:00Z",
        }

        # Produce a message
        await producer.send_and_wait("user_service", json.dumps(user_data).encode("utf-8"))

        # Consume a message
        async for msg in consumer:
            received_data = json.loads(msg.value.decode("utf-8"))
            assert received_data == user_data
            break
    finally:
        await producer.stop()
        await consumer.stop()

async def retry_connection(coroutine, retries=5, delay=2):
    for i in range(retries):
        try:
            await coroutine()
            return
        except KafkaConnectionError:
            if i == retries - 1:
                raise
            await asyncio.sleep(delay)
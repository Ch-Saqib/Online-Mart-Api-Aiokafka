from services.order_consumer import consume_order
from services.notification_consumer import *
from contextlib import asynccontextmanager
from services.transaction_consumer import *
from typing import AsyncGenerator
from services.consumers import *
from fastapi import FastAPI
from router import *
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Creating Tables.........")
    create_db_and_tables()
    print("Starting consumer.....")
    asyncio.create_task(consume("user_service", "broker:19092"))
    asyncio.create_task(consume_order("order_service", "broker:19092"))
    asyncio.create_task(consume_notification("notification_service", "broker:19092"))
    asyncio.create_task(consume_transaction("transaction_service", "broker:19092"))

    yield
    print("Stopping consumer")


app: FastAPI = FastAPI(lifespan=lifespan, title="USER MANGEMENT API", root_path="/user")


@app.get("/")
def root():
    return {"message": "Hello World From User Mangement"}


# User
app.include_router(user_router, tags=["User"])
# Login
app.include_router(login_router, tags=["Login"])

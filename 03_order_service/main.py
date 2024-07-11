from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from services.consumers import *
from services.notification_consumer import *
import asyncio
from router import *


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Creating Tables.........")
    create_tables()
    print("Tables created")
    print("Starting Kafka Consumers.....")
    asyncio.create_task(
        consume_order(topic="order_service", bootstrap_servers="broker:19092")
    )
    asyncio.create_task(
        consume_orderitems(
            topic="order_items_service", bootstrap_servers="broker:19092"
        )
    )
    asyncio.create_task(
        consume_shipments(topic="shipment_service", bootstrap_servers="broker:19092")
    )
    asyncio.create_task(
        consume_notification(
            topic="notification_service", bootstrap_servers="broker:19092"
        )
    )

    yield


app: FastAPI = FastAPI(lifespan=lifespan, title="Order Service", root_path="/order")


@app.get("/")
def root():
    return {"message": "Hello World From Order Service"}


# Order
app.include_router(order_router, tags=["Order"])
# Orderitem
app.include_router(orderitem_router, tags=["OrderItem"])
# Shipment
app.include_router(shipment_router, tags=["Shipment"])

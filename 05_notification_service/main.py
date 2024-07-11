from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from services.consumers import *
from router import *
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Creating Tables....")
    create_tables()
    print("Starting Consumers....")
    asyncio.create_task(
        consume_notification(
            topic="notification_service", bootstrap_servers="broker:19092"
        )
    )
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="Notification Service", root_path="/notification"
)


@app.get("/")
def root():
    return {"message": "Hello World From Notification Service"}


# Notification
app.include_router(notification_router, tags=["Notification"])

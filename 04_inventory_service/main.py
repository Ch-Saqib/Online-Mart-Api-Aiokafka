from fastapi import FastAPI, Depends
from database import *
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio
from services.inventory_consumer import *
from services.consumers import *
from router import *


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # startup code goes here
    print("Creating Tables.........")
    create_tables()  # Call the function to create tables
    print("Consumer Started ....")
    asyncio.create_task(consume_location("location_service", "broker:19092"))
    asyncio.create_task(consume_inventory("inventory_service", "broker:19092"))
    # asyncio.create_task(stockmovement_consume("stockmovement_service", "broker:19092"))
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="Inventory Services", root_path="/inventory"
)


@app.get("/")
def root():
    return {"message": "Hello World From Inventory Service"}


# Location
app.include_router(location_router, tags=["Location"])
# Inventory
app.include_router(inventory_router, tags=["Inventory"])

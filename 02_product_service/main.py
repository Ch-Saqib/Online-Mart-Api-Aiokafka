import asyncio
from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from services.inventory_consumer import *
from services.order_consumer import *
from services.consumers import *
from router import *


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Creating Tables............")
    create_tables()
    print("Starting consumer")
    asyncio.create_task(consume_product("product_service", "broker:19092"))
    asyncio.create_task(consume_category("category_service", "broker:19092"))
    asyncio.create_task(consume_review("review_service", "broker:19092"))
    asyncio.create_task(consume_rating("rating_service", "broker:19092"))
    asyncio.create_task(consume_inventory("inventory_service", "broker:19092"))
    asyncio.create_task(consume_orderitem("order_items_service", "broker:19092"))
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="Product Services ", root_path="/product"
)


@app.get("/")
def get_data():
    return {"message": "Hello World From Products Service"}


# Category
app.include_router(category_router, tags=["Category"])
# Product
app.include_router(product_router, tags=["Product"])
# Rating
app.include_router(rating_router, tags=["Rating"])
# Review
app.include_router(review_router, tags=["Review"])

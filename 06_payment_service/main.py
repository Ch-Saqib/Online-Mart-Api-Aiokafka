from fastapi import FastAPI
from services.payment_service import *
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from services.consumers import *
from router import *
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("Tables Creating........")
    create_tables()
    print("Consumers Started........")

    asyncio.create_task(
        consume_transaction(
            topic="transaction_service", bootstrap_servers="broker:19092"
        )
    )
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan, title="Payment Services", root_path="/payment"
)


@app.get("/")
def root():
    return {"message": "Hello World From Payment Service"}


# Transaction
app.include_router(transaction_router, tags=["Transaction"])

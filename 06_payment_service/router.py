from aiokafka import AIOKafkaProducer
from fastapi import Depends, APIRouter
from services.payment_service import *
from database import *
from models import *
from typing import Annotated
from services.consumers import *
import payment_pb2

transaction_router = APIRouter()


# Crud Transaction
@transaction_router.get("/transactions")
def get_all_transactions(session: Annotated[Session, Depends(get_session)]):
    return get_transactions(session=session)


@transaction_router.get("/transactions/{transaction_id}")
def get_transaction_by_id(
    transaction_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_transaction_id(transaction_id=transaction_id, session=session)


@transaction_router.post("/create-payment-intent")
async def create_payment(
    user_id: int,
    payment_request: PaymentRequest,
):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        add_transaction = payment_pb2.Transaction_Proto(
            user_id=user_id,
            amount=payment_request.amount,
            currency=payment_request.currency,
            description=payment_request.description,
            payment_method=payment_request.payment_method,
        )
        # Serialize Data
        protoc_data = add_transaction.SerializeToString()
        # Produce message
        await producer.send_and_wait("transaction_service", protoc_data)
        return {"user_id": user_id, "Payment Intent": payment_request}
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@transaction_router.put("/transactions_update/{transaction_id}")
def update_transaction_by_id(
    transaction_id: int,
    transaction_update: PaymentUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_transaction(
        transaction_id=transaction_id,
        transaction_update=transaction_update,
        session=session,
    )


@transaction_router.delete("/transactions_delete/{transaction_id}")
def delete_transaction_by_id(
    transaction_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_transaction(transaction_id=transaction_id, session=session)

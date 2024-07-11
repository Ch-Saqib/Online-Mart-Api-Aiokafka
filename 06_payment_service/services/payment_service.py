from fastapi import HTTPException
from database import *
from models import *
import stripe
import payment_pb2

# Set your secret key from Stripe dashboard
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def get_transactions(session: Session):
    try:
        statement = session.exec(select(Transaction)).all()
        return {"transactions": statement}
    except Exception as e:
        return {"error": str(e)}


def get_transaction_id(transaction_id: int, session: Session):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def create_payment_intent(
    payment_request: payment_pb2.Transaction_Proto, session: Session, user_id: int
):
    try:
        # Create a payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=payment_request.amount,
            currency=payment_request.currency,
            description=payment_request.description,
            payment_method=payment_request.payment_method,
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
            metadata={"user_id": user_id},
        )

        # Store the transaction in the database
        transaction = Transaction(
            stripe_id=intent.id,
            user_id=user_id,
            amount=intent.amount,
            currency=intent.currency,
            description=intent.description,
            status=intent.status,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return {"status": "success", "payment_intent": intent}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_transaction(
    transaction_id: int, transaction_update: PaymentUpdate, session: Session
):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        update_data = transaction_update.model_dump(exclude_unset=True)
        get_data.sqlmodel_update(update_data)
        session.commit()
        session.refresh(get_data)
        return {"message": "Data Updated Successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def delete_transaction(transaction_id: int, session: Session):
    try:
        get_data = session.get(Transaction, transaction_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(get_data)
        session.commit()
        return {"message": "Transaction Deleted Successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

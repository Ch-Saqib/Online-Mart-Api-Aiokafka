from sqlmodel import SQLModel

class PaymentRequest(SQLModel):
    amount: int
    currency: str
    description: str
    payment_method: str  # pm_card_visa


class PaymentUpdate(SQLModel):
    amount: int = None
    currency: str = None
    description: str = None
    payment_method: str = None  # pm_card_visa

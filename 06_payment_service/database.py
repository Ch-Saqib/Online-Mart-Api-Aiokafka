from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from dotenv import load_dotenv
import os

load_dotenv()


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    stripe_id: str
    user_id: int
    amount: int
    currency: str
    description: str
    status: str
    transaction_date: datetime = Field(default_factory=datetime.utcnow)

# Creating the database engine
DATABASE_URL = os.getenv("DATABASE_URL_6")
engine = create_engine(DATABASE_URL)


# Creating the tables
def create_tables():
    SQLModel.metadata.create_all(engine)


# Get Session Method
def get_session():
    with Session(engine) as session:
        yield session

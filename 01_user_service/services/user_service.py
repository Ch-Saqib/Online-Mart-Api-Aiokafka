from models import *
from sqlmodel import select, Session, create_engine
from fastapi import Depends, HTTPException
from typing import Annotated, List
from dotenv import load_dotenv
import bcrypt
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import User
from datetime import datetime
import user_pb2


load_dotenv()


# In-memory token blacklist
blacklisted_tokens: List[str] = []

DATABASE_USER_SERVICE_URL: str = os.getenv("DATABASE_URL_1")
engine_user = create_engine(DATABASE_USER_SERVICE_URL)


def get_session():
    with Session(engine_user) as session:
        yield session


ALGORITHM = "HS256"

SECRET_KEY = "This is secret key"


# ENCODE DATA
def create_access_token(subject: str, delta_time: timedelta) -> str:
    expire_time = datetime.utcnow() + delta_time
    to_encode = {"exp": expire_time, "sub": subject}
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


# DECODE DATA


def decode_access_token(subject: str):

    try:
        decode_jwt = jwt.decode(subject, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_jwt

    except JWTError as error:
        return {"Error:": error}


# Password Hashing


def get_password_hash(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


# Verify Password


def verify_password(plain_password: str, hashed_password: str) -> str:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Create Data
async def create_user(
    user: user_pb2.User_Proto, session: Annotated[Session, Depends(get_session)]
) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
        created_at=user.created_at,
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except HTTPException as error:
        raise error


# Verify Email
def get_user_by_email(
    email: str, db: Annotated = [Session, Depends(get_session)]
) -> User:
    try:
        statement = db.get(User, email)
        return statement
    except:
        return None


# Verify Username
def get_user_by_username(
    username: str, db: Annotated = [Session, Depends(get_session)]
) -> User:
    try:
        statement = db.exec(select(User).where(User.username == username)).first()
        return statement
    except:
        return None


# Verify Token
def verify_token(token: str):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    decoded_data = decode_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return decoded_data


# Get All Data
def get_all_users(db: Session) -> List[User]:
    statement = select(User)
    users = db.exec(statement).all()
    return users


def forget_password(email: str, db: Session) -> User:
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def validate_by_id(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

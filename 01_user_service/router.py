from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException, Depends, APIRouter
from aiokafka import AIOKafkaProducer
from services.user_service import *
from datetime import timedelta
from typing import Annotated
from database import *
from models import *

login_router = APIRouter()
user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Signup
@user_router.post("/signup")
async def signup(user: UserCreate, db: Annotated[Session, Depends(get_session)]):
    db_user = get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")

    await producer.start()

    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(user.created_at)

        user_data = user_pb2.User_Proto(
            username=user.username,
            email=user.email,
            password=user.password,
            role=user.role,
            created_at=created_at_str,
        )
        protoc_data = user_data.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")

        # Produce the message to Kafka
        await producer.send_and_wait("user_service", protoc_data)

        return user
    finally:
        await producer.stop()


# Login
@login_router.post("/login")
async def login(
    db: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
):
    db_user = get_user_by_username(username=form_data.username, db=db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email Not Registered")
    if not verify_password(
        plain_password=form_data.password, hashed_password=db_user.password
    ):
        raise HTTPException(status_code=400, detail="Incorrect Password")

    expire_time = timedelta(minutes=30)
    access_token = create_access_token(subject=db_user.username, delta_time=expire_time)
    return {"access_token": access_token}


# Get Data With Token
@login_router.get("/get_data_with_token")
async def get_data_with_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_session)],
):
    decoded_data = decode_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = decoded_data.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    db_user = get_user_by_username(username=username, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_data": db_user}


# Signout
@user_router.delete("/signout")
async def signout(
    token: str,
    db: Annotated[Session, Depends(get_session)],
):
    decoded_data = verify_token(token)
    email = decoded_data.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    db_user = get_user_by_email(email=email, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the token to the blacklist
    blacklisted_tokens.append(token)

    return {"message": "User signed out successfully"}


# Refresh Token
@user_router.get("/refresh")
async def refresh(token: str, db: Annotated[Session, Depends(get_session)]):
    decoded_data = verify_token(token)
    email = decoded_data.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    db_user = get_user_by_email(email=email, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a new access token
    expire_time = timedelta(minutes=30)
    new_access_token = create_access_token(
        subject=db_user.email, delta_time=expire_time
    )

    return {"refresh_access_token": new_access_token}


# Forget Password
@user_router.get("/forget_password/{email}")
def forget_passwords(email: str, db: Annotated[Session, Depends(get_session)]):
    user = forget_password(email=email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    expire_time = timedelta(minutes=30)
    reset_token = create_access_token(subject=user.email, delta_time=expire_time)
    return {"access token": reset_token}


# Reset Password
@user_router.put("/reset")
async def reset_password(
    token: str,
    new_password: str,
    db: Annotated[Session, Depends(get_session)],
):
    decoded_data = decode_access_token(token)
    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = decoded_data.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    db_user = get_user_by_email(email=email, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    hashed = hashed_password.decode("utf-8")

    db_user.password = hashed

    db.commit()
    db.refresh(db_user)
    return {"message": "Password reset successfully"}


# Get All Users
@login_router.get("/get_all_users")
def get_all_user(db: Annotated[Session, Depends(get_session)]):
    users = get_all_users(db=db)
    return users

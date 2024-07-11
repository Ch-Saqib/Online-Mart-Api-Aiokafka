from fastapi import FastAPI, Depends, APIRouter
from models import *
from database import *
from aiokafka import AIOKafkaProducer
from datetime import datetime
from services.product_service import *
from services.inventory_consumer import *
from services.order_consumer import *
from services.consumers import *
import product_pb2

category_router = APIRouter()
product_router = APIRouter()
review_router = APIRouter()
rating_router = APIRouter()


# # Category Crud Opreation Api
@category_router.get("/get_category", response_model=List[Category])
def get_categories(session: Annotated[Session, Depends(get_session)]):
    return get_category(session=session)


@category_router.get("/category_by_id/{category_id}", response_model=Category)
def get_category_by_id(
    category_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_category_id(category_id=category_id, session=session)


@category_router.post("/add_category")
async def create_category(category: CategoryAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        # Produce message
        add_category = product_pb2.Category_Proto(
            name=category.name,
            description=category.description,
        )
        protoc_data = add_category.SerializeToString()
        # print("Serialized : ", protoc_data)
        await producer.send_and_wait("category_service", protoc_data)
        if not add_category:
            return {"message": "Category not added"}

        return "Message Sent"

    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@category_router.put("/category_update/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_category_by_id(
        category_id=category_id, category_update=category, session=session
    )


@category_router.delete("/category_delete/{category_id}")
def delete_category(
    category_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_category_by_id(category_id=category_id, session=session)


# Product Crud opreation Api



@product_router.get("/get_product", response_model=List[Product])
def get_products(session: Annotated[Session, Depends(get_session)]):
    return get_product(session=session)


@product_router.get("/product_by_id/{product_id}", response_model=Product)
def get_product_by_id(
    product_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_product_id(product_id=product_id, session=session)


@product_router.post("/add_product", response_model=Product)
async def create_product(
    product: ProductAdd,
):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Convert datetime to google.protobuf.Timestamp
        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(product.created_at)
        updated_at_str = datetime_to_iso(product.updated_at)

        # Produce message
        add_data = product_pb2.Product_Proto(
            name=product.name,
            description=product.description,
            price=product.price,
            available=product.available,
            category_id=product.category_id,
            created_at=created_at_str,
            updated_at=updated_at_str,
        )
        protoc_data = add_data.SerializeToString()
        # print("Serialized : ", protoc_data)
        await producer.send_and_wait("product_service", protoc_data)
        if not add_data:
            return {"message": "Product not added"}

        return product

    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@product_router.put("/product_update/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_product_by_id(
        product_id=product_id, product_update=product, session=session
    )


@product_router.delete("/product_delete/{product_id}")
def delete_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    return delete_product_by_id(product_id=product_id, session=session)


# # Rating Crud Opreation Api
@rating_router.get("/get_rating", response_model=List[Rating])
def get_ratings(session: Annotated[Session, Depends(get_session)]):
    return get_rating(session=session)


@rating_router.get("/rating_by_id/{rating_id}", response_model=Rating)
def get_rating_by_id(rating_id: int, session: Annotated[Session, Depends(get_session)]):
    return get_rating_id(rating_id=rating_id, session=session)


@rating_router.post("/add_rating")
async def create_rating(rating: RatingAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(rating.created_at)

        # Produce message
        add_rating = product_pb2.Rating_Proto(
            rating=rating.rating,
            product_id=rating.product_id,
            created_at=created_at_str,
        )
        protoc_data = add_rating.SerializeToString()
        # print("Serialized : ", protoc_data)
        await producer.send_and_wait("rating_service", protoc_data)
        if not add_rating:
            return {"message": "Rating not added"}

        return "Message Sent"

    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@rating_router.put("/rating_update/{rating_id}", response_model=Rating)
def update_rating(
    rating_id: int,
    rating: RatingUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_rating_by_id(
        rating_id=rating_id, rating_update=rating, session=session
    )


@rating_router.delete("/rating_delete/{rating_id}")
def delete_rating(rating_id: int, session: Annotated[Session, Depends(get_session)]):
    return delete_rating_by_id(rating_id=rating_id, session=session)


# # Review Crud Opreation Api
@review_router.get("/get_review", response_model=List[Review])
def get_reviews(session: Annotated[Session, Depends(get_session)]):
    return get_review(session=session)


@review_router.get("/review_by_id/{review_id}", response_model=Review)
def get_review_by_id(review_id: int, session: Annotated[Session, Depends(get_session)]):
    return get_review_id(review_id=review_id, session=session)


@review_router.post("/add_review")
async def create_review(review: ReviewAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(review.created_at)

        # Produce message
        add_review = product_pb2.Review_Proto(
            review_text=review.review_text,
            product_id=review.product_id,
            created_at=created_at_str,
        )
        protoc_data = add_review.SerializeToString()
        # print("Serialized : ", protoc_data)
        await producer.send_and_wait("review_service", protoc_data)
        if not add_review:
            return {"message": "Review not added"}

        return "Message Sent"

    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@review_router.put("/review_update/{review_id}", response_model=Review)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_review_by_id(
        review_id=review_id, review_update=review, session=session
    )


@review_router.delete("/review_delete/{review_id}")
def delete_review(review_id: int, session: Annotated[Session, Depends(get_session)]):
    return delete_review_by_id(review_id=review_id, session=session)

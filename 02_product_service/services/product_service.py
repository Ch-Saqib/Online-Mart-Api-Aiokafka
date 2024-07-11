from sqlmodel import Session, select
from models import *
from fastapi import HTTPException
from database import Product, Category, Review, Rating
import product_pb2
from google.protobuf.json_format import ParseDict


# Product Crud Opreation
def get_product(session: Session):
    try:
        get_data = session.exec(select(Product)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_product_id(product_id: int, session: Session) -> Product:
    try:
        get_data = session.get(Product, product_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Product not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_product(product: product_pb2.Product_Proto, session: Session):
    # Convert protobuf data to Product model
    # db_product=product.model_dump(exclude_unset=True)
    # ParseDict(db_product)
    validate_category_id = session.get(Category, product.category_id)
    if validate_category_id is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        available=product.available,
        category_id=product.category_id,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )

    try:
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return {"message": "Product added successfully"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def update_product_by_id(
    product_id: int, product_update: ProductUpdate, session: Session
):
    # Step 1: Get the Product by ID
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    hero_data = product_update.model_dump(exclude_unset=True)
    product.sqlmodel_update(hero_data)
    session.add(product)
    session.commit()
    return product


def delete_product_by_id(product_id: int, session: Session):
    # Step 1: Get the Product by ID
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Delete the Product
    session.delete(product)
    session.commit()
    return {"message": "Product Deleted Successfully"}


def validate_product_id(product_id: int, session: Session):
    try:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# # Category Crud Opreation


def get_category(session: Session):
    try:
        get_data = session.exec(select(Category)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_category_id(category_id: int, session: Session):
    try:
        get_data = session.get(Category, category_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Product not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_category(category: product_pb2.Category_Proto, session: Session):
    try:
        db_user = Category(
            name=category.name,
            description=category.description,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_category_by_id(
    category_id: int, product_update: CategoryUpdate, session: Session
):
    # Step 1: Get the Product by ID
    product = session.get(Category, category_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    hero_data = product_update.model_dump(exclude_unset=True)
    product.sqlmodel_update(hero_data)
    session.add(product)
    session.commit()
    return product


def delete_category_by_id(category_id: int, session: Session):
    # Step 1: Get the Product by ID
    product = session.get(Category, category_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Delete the Product
    session.delete(product)
    session.commit()
    return {"message": "Category Deleted Successfully"}


# # Review Crud Opreation
def get_review(session: Session):
    try:
        get_data = session.exec(select(Review)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_review_id(review_id: int, session: Session):
    try:
        get_data = session.get(Review, review_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Review not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_review(session: Session, review: product_pb2.Review_Proto) -> Review:
    try:
        validate_product_id = session.get(Product, review.product_id)
        if validate_product_id is None:
            raise HTTPException(status_code=404, detail="Product not found")
        db_user = Review(
            review_text=review.review_text,
            product_id=review.product_id,
            created_at=review.created_at,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_review_by_id(review_id: int, review_update: ReviewUpdate, session: Session):
    # Step 1: Get the Product by ID
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Step 2: Update the Product
    hero_data = review_update.model_dump(exclude_unset=True)
    review.sqlmodel_update(hero_data)
    session.add(review)
    session.commit()
    return review


def delete_review_by_id(review_id: int, session: Session):
    # Step 1: Get the Product by ID
    review = session.get(Review, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Step 2: Delete the Product
    session.delete(review)
    session.commit()
    return {"message": "Review Deleted Successfully"}


# # Rating Crud Opreation
def get_rating(session: Session):
    try:
        get_data = session.exec(select(Rating)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_rating_id(rating_id: int, session: Session):
    try:
        get_data = session.get(Rating, rating_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Rating not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_rating(session: Session, rating: product_pb2.Rating_Proto):
    try:
        validate_product_id = session.get(Product, rating.product_id)
        if validate_product_id is None:
            raise HTTPException(status_code=404, detail="Product not found")
        db_user = Rating(
            rating=rating.rating,
            product_id=rating.product_id,
            created_at=rating.created_at,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_rating_by_id(rating_id: int, rating_update: RatingUpdate, session: Session):
    # Step 1: Get the Product by ID
    rating = session.get(Rating, rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    # Step 2: Update the Product
    hero_data = rating_update.model_dump(exclude_unset=True)
    rating.sqlmodel_update(hero_data)
    session.add(rating)
    session.commit()
    return rating


def delete_rating_by_id(rating_id: int, session: Session):
    # Step 1: Get the Product by ID
    rating = session.get(Rating, rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    # Step 2: Delete the Product
    session.delete(rating)
    session.commit()
    return {"message": "Rating Deleted Successfully"}

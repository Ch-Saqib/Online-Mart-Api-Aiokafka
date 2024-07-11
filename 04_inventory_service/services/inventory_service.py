from fastapi import HTTPException
from models import *
from sqlmodel import Session, select
from database import *
import inventory_pb2


# Crud Location
def get_location(session: Session):
    try:
        get_data = session.exec(select(Location)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_location_id(location_id: int, session: Session):
    try:
        get_data = session.get(Location, location_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Location not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_location(location: inventory_pb2.Location_Proto, session: Session):
    try:
        db_user = Location(
            location_name=location.location_name,
            address=location.address,
            created_at=location.created_at,
            updated_at=location.updated_at,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_location_by_id(
    location_id: int, location_update: LocationUpdate, session: Session
):
    try:
        # Step 1: Get the Product by ID
        product = session.get(Location, location_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Location not found")
        # Step 2: Update the Product
        location_data = location_update.model_dump(exclude_unset=True)
        product.sqlmodel_update(location_data)
        session.add(product)
        session.commit()
        return {"Location Updated Successfully"}
    # return {"message": "Product updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_location_by_id(location_id: int, session: Session):
    try:
        location = session.get(Location, location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        session.delete(location)
        session.commit()
        return {"message": "Location deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crud inventory
def get_inventory(session: Session):
    try:
        get_data = session.exec(select(Inventory)).all()
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_inventory_id(inventory_id: int, session: Session):
    try:
        get_data = session.get(Inventory, inventory_id)
        if not get_data:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return get_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def add_inventory(inventory: inventory_pb2.Inventory_Proto, session: Session):
    try:
        validate_location_id = session.get(Location, inventory.location_id)
        if validate_location_id is None:
            raise HTTPException(status_code=404, detail="Location not found")
        db_user = Inventory(
            location_id=inventory.location_id,
            product_id=inventory.product_id,
            quantity=inventory.quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_inventory_by_id(
    inventory_id: int, inventory_update: InventoryUpdate, session: Session
):
    try:
        # Step 1: Get the Product by ID
        inventory = session.get(Inventory, inventory_id)
        if inventory is None:
            raise HTTPException(status_code=404, detail="Inventory not found")
        # Step 2: Update the Product
        hero_data = inventory_update.model_dump(exclude_unset=True)
        inventory.sqlmodel_update(hero_data)
        session.add(inventory)
        session.commit()
        return {"message": "Inventory updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_inventory_by_id(inventory_id: int, session: Session):
    try:
        inventory = session.get(Inventory, inventory_id)
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")
        session.delete(inventory)
        session.commit()
        return {"message": "Inventory deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crud StockMovement
# def get_stock_movement(session: Session):
#     try:
#         get_data = session.exec(select(StockMovement)).all()
#         return get_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def get_stock_movement_id(stock_movement_id: int, session: Session):
#     try:
#         get_data = session.get(StockMovement, stock_movement_id)
#         if not get_data:
#             raise HTTPException(status_code=404, detail="StockMovement not found")
#         return get_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# async def add_stock_movement(
#     stock_movement: inventory_pb2.StockMovement_Proto, session: Session
# ):
#     try:
#         db_user = StockMovement(
#             inventory_id=stock_movement.inventory_id,
#             quantity=stock_movement.quantity,
#             movement_type=stock_movement.movement_type,
#             reference_id=stock_movement.reference_id,
#             created_at=stock_movement.created_at,
#             updated_at=stock_movement.updated_at,
#         )
#         session.add(db_user)
#         session.commit()
#         session.refresh(db_user)
#         return db_user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def update_stock_movement_by_id(
#     movement_id: int, stock_movement_update: StockMovementUpdate, session: Session
# ):
#     try:
#         # Step 1: Get the Product by ID
#         stock_movement = session.exec(
#             select(StockMovement).where(StockMovement.movement_id == movement_id)
#         ).one_or_none()
#         if stock_movement is None:
#             raise HTTPException(status_code=404, detail="StockMovement not found")
#         # Step 2: Update the Product
#         stock_movement_data = stock_movement_update.model_dump(exclude_unset=True)
#         stock_movement.sqlmodel_update(stock_movement_data)
#         session.add(stock_movement)
#         session.commit()
#         return {"StockMovement Updated Successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# def delete_stock_movement_by_id(stock_movement_id: int, session: Session):
#     try:
#         stock_movement = session.get(StockMovement, stock_movement_id)
#         if not stock_movement:
#             raise HTTPException(status_code=404, detail="StockMovement not found")
#         session.delete(stock_movement)
#         session.commit()
#         return {"message": "StockMovement deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

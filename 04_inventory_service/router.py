from aiokafka import AIOKafkaProducer
from fastapi import Depends, APIRouter
from database import *
from contextlib import asynccontextmanager
from services.inventory_service import *
from typing import Annotated
import inventory_pb2
from services.inventory_consumer import *
from services.consumers import *

location_router = APIRouter()
inventory_router = APIRouter()


# Crud location
@location_router.get("/get_location", response_model=list[Location])
def get_locations(session: Annotated[Session, Depends(get_session)]):
    return get_location(session=session)


@location_router.post("/create_location")
async def add_locations(location: LocationAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(location.created_at)
        updated_at_str = datetime_to_iso(location.updated_at)
        # Produce message
        add_inventory = inventory_pb2.Location_Proto(
            location_name=location.location_name,
            address=location.address,
            created_at=created_at_str,
            updated_at=updated_at_str,
        )
        protoc_data = add_inventory.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")
        await producer.send_and_wait("location_service", protoc_data)

        return location
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@location_router.get("/get_location_by_id/{location_id}")
def get_location_by_id(
    location_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_location_id(location_id=location_id, session=session)


@location_router.put("/location_update/{location_id}")
def update_location(
    location_id: int,
    location_update: LocationUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_location_by_id(
        location_id=location_id, location_update=location_update, session=session
    )


@location_router.delete("/delete_location_by_id/{location_id}")
def delete_location_id(
    location_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_location_by_id(location_id=location_id, session=session)


# Crud inventory


@inventory_router.get("/get_inventory")
def get_inventories(session: Annotated[Session, Depends(get_session)]):
    return get_inventory(session=session)


@inventory_router.post("/create_inventory")
async def add_inventories(inventory: InventoryAdd):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:

        def datetime_to_iso(dt: datetime) -> str:
            return dt.isoformat()

        created_at_str = datetime_to_iso(inventory.created_at)
        updated_at_str = datetime_to_iso(inventory.updated_at)
        # Produce message
        add_inventory = inventory_pb2.Inventory_Proto(
            location_id=inventory.location_id,
            product_id=inventory.product_id,
            quantity=inventory.quantity,
            created_at=created_at_str,
            updated_at=updated_at_str,
        )
        protoc_data = add_inventory.SerializeToString()
        print(f"Serialized Data : {protoc_data} ")
        await producer.send_and_wait("inventory_service", protoc_data)
        return inventory
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


@inventory_router.get("/get_inventory_by_id/{inventory_id}")
def get_inventory_by_id(
    inventory_id: int, session: Annotated[Session, Depends(get_session)]
):
    return get_inventory_id(inventory_id=inventory_id, session=session)


@inventory_router.put("/update_inventory_by_id/{inventory_id}")
def update_inventory_id(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    return update_inventory_by_id(
        inventory_id=inventory_id, inventory_update=inventory_update, session=session
    )


@inventory_router.delete("/delete_inventory_by_id/{inventory_id}")
def delete_inventory_id(
    inventory_id: int, session: Annotated[Session, Depends(get_session)]
):
    return delete_inventory_by_id(inventory_id=inventory_id, session=session)

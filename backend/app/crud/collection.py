from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, or_
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.collection import Collection, CollectionStatus, collections_collection_types
from app.models.address import Address
from app.models.schedule import Schedule
from app.models.collection_type import WasteType, CollectionType
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse, CollectionsAllRequest, CollectionAddressResponse
from app.schemas.address import AddressResponse
from app.apis.nyc_311 import get_collection_status
from datetime import datetime, timedelta
from app.database import SessionLocal


def get_collection_status_api() -> tuple[CollectionStatus, CollectionStatusResponse]:
    """" Get collection status from 311 API"""
    # tomorrow = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
    tomorrow = datetime(2025, 7, 9).strftime("%m/%d/%Y")

    collection_status = get_collection_status(CollectionStatusRequest(
        from_date=tomorrow,
        to_date=tomorrow
    ))
    # failed response set collection event as unknown
    status_options = [status.value for status in CollectionStatus]
    if (
        collection_status.status == "failed"
        or len(collection_status.data) == 0
        or collection_status.data[0].get("status") not in status_options
            ):
        collection_status_value = CollectionStatus.unknown
    else:
        collection_status_value = CollectionStatus(collection_status.data[0].get("status"))
    return collection_status_value, collection_status


def get_address_data_for_collection() -> list[CollectionAddressResponse]:
    """ Get collection data needed to create collections"""
    day_of_week = datetime(2025, 7, 9).strftime("%A").lower()
    # day_of_week = (datetime.today() + timedelta(days=1)).strftime("%A").lower()
    set_collections = []
    # day_of_week = "wednesday"
    # print(day_of_week)
    db = SessionLocal()
    addresses = db.execute(select(Address).join(
        Schedule, Address.schedule_id == Schedule.id
        ).where(
        or_(Schedule.days_trash.contains([day_of_week]),
            Schedule.days_recycling.contains([day_of_week]),
            Schedule.days_compost.contains([day_of_week]),
            Schedule.days_large_items.contains([day_of_week]))
    )).scalars().all()
    for address in addresses:
        validated_address = CollectionAddressResponse.model_validate(address)
        if day_of_week in address.schedule.days_trash:
            validated_address.collection_types.append(WasteType.trash)
        if day_of_week in address.schedule.days_recycling:
            validated_address.collection_types.append(WasteType.recycling)
        if day_of_week in address.schedule.days_compost:
            validated_address.collection_types.append(WasteType.compost)
        if day_of_week in address.schedule.days_large_items:
            validated_address.collection_types.append(WasteType.large_items)
        set_collections.append(validated_address)
    db.close()
    return set_collections


def update_collection_event():
    """ Update collection events that were previously delayed, suspended"""
    db = SessionLocal()
    # tomorrow = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
    tomorrow = datetime(2025, 7, 9).strftime("%m/%d/%Y")
    next_day = datetime(2025, 7, 10).strftime("%m/%d/%Y")
    print(datetime.strptime(tomorrow, "%m/%d/%Y") - timedelta(days=7))
    delayed_collections = db.execute(select(Collection).where(
        Collection.status != CollectionStatus.on_schedule,
        Collection.updated_collection_date == tomorrow
    )).scalars().all()
    collection_status_value, collection_status = get_collection_status_api()
    # set on schedule if resumed sanitation collection
    for collection in delayed_collections:
        if collection_status_value == CollectionStatus.on_schedule:
            db.execute(update(Collection).where(
                Collection.id == collection.id).values(
                    status=CollectionStatus.on_schedule
                ))
        else:
            db.execute(update(Collection).where(
                Collection.id == collection.id).values(
                    status=collection_status_value,
                    delay_reason=collection_status.data[0].get("details"),
                    updated_collection_date=next_day
                    ))
    db.commit()
    db.close()


def create_collection_event():
    """ Create collection event for each user depending on address schedules"""
    collection_data = get_address_data_for_collection()
    # tomorrow = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
    # next_day = (datetime.today() + timedelta(days=2)).strftime("%m/%d/%Y")
    tomorrow = datetime(2025, 7, 9).strftime("%m/%d/%Y")
    next_day = datetime(2025, 7, 10).strftime("%m/%d/%Y")
    collection_status_value, collection_status = get_collection_status_api()
    print(collection_status)
    print(collection_status_value)
    db = SessionLocal()
    collection_types_query = db.execute(select(CollectionType)).scalars().all()
    map_collection_types = {
    }
    for col_types in collection_types_query:
        map_collection_types[col_types.waste_type] = col_types
    for collection in collection_data:
        collection_exists_query = db.execute(
            select(Collection).where(
                collection.id == Collection.address_id,
                or_(tomorrow == Collection.updated_collection_date,
                    next_day == Collection.updated_collection_date),
                )).scalar_one_or_none()
        if collection_exists_query:
            continue
        on_schedule = collection_status_value == CollectionStatus.on_schedule
        collection_event = Collection(
            schedule_id=collection.schedule_id,
            address_id=collection.id,
            collection_date=tomorrow,
            status=collection_status_value,
            updated_collection_date=tomorrow if on_schedule else next_day,
            collection_types=[map_collection_types[col_type] for col_type in collection.collection_types],
            delay_reason=None if on_schedule else collection_status.data[0].get("details")
        )
        try:
            db.add(collection_event)
            db.commit()
        except IntegrityError:
            db.rollback()
        print(collection)
    db.close()


def delete_collection_event():
    """ Delete collection events older than 2 weeks"""
    db = SessionLocal()
    print(datetime.today() - timedelta(days=14))
    db.execute(delete(Collection).where(
        Collection.collection_date < datetime.today() - timedelta(days=14)
            ))
    db.commit()
    db.close()


if __name__ == "__main__":
    # delete_collection_event()
    update_collection_event()
    create_collection_event()

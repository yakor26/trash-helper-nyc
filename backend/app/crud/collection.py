from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.models.user import User
from app.models.collection import Collection
from app.models.address import Address
from app.models.schedule import Schedule
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse
from app.apis.nyc_311 import get_collection_status
from datetime import datetime
from app.database import SessionLocal


def get_data_for_collection():
    """ Get collection data needed to create collections"""
    # day_of_week = datetime.today().strftime("%A").lower()
    day_of_week = datetime(2026, 6, 3).strftime("%A").lower()
    print(day_of_week)
    db = SessionLocal()
    address = db.execute(select(Address).join(
        Schedule, Address.schedule_id == Schedule.id
        ).where(
        Schedule.days_trash.contains([day_of_week])
    )).scalars().all()
    print(len(address))
    print(address)
    # addresses = db.execute(select(Address)).scalars().all()
    # for address in addresses:
    #     is_trash_day = day_of_week in address.schedule.days_trash
    #     is_recycling_day = day_of_week in address.schedule.days_recycling
    #     is_compost_day = day_of_week in address.schedule.days_compost
    #     is_large_items_day = day_of_week in address.schedule.days_large_items
    #     print(is_trash_day, is_recycling_day, is_compost_day, is_large_items_day)
    # users = db.execute(select(User)).scalars().all()
    # for user in users:
    #     for address in user.addresses:
    #         is_trash_day = day_of_week in address.schedule.days_trash
    #         is_recycling_day = day_of_week in address.schedule.days_recycling
    #         is_compost_day = day_of_week in address.schedule.days_compost
    #         is_large_items_day = day_of_week in address.schedule.days_large_items
    #         print(is_trash_day, is_recycling_day, is_compost_day, is_large_items_day)

def create_collection_event():
    """ Create collection event for each user depending on address schedules"""
    pass
    

if __name__ == "__main__":
    get_data_for_collection()
    create_collection_event()

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.models.user import User
from app.models.collection import Collection
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse
from app.apis.nyc_311 import get_collection_status
from datetime import datetime
from app.database import SessionLocal


def create_collection_event():
    """ Create collection event for each user depending on address schedules"""

    day_of_week = datetime.today().strftime("%A").lower()
    db = SessionLocal()
    users = db.execute(select(User)).scalars().all()
    for user in users:
        for address in user.addresses:
            is_trash_day = day_of_week in address.schedule.days_trash
            is_recycling_day = day_of_week in address.schedule.days_recycling
            is_compost_day = day_of_week in address.schedule.days_compost
            is_large_items_day = day_of_week in address.schedule.days_large_items
            print(is_trash_day, is_recycling_day, is_compost_day, is_large_items_day)
if __name__ == "__main__":
    create_collection_event()

from app.models.notification import Notification
from app.schemas.notification import TextNotificationRequest
from app.models.collection import Collection, CollectionStatus
from app.models.collection_type import CollectionType
from app.models.address import Address
from app.models.user import User
from sqlalchemy import select, update, delete, or_, and_
from app.database import SessionLocal
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app.apis.text_notifications import send_text
from sqlalchemy.orm import Session


def create_notification_message(
        col_types: list[CollectionType],
        col_status: CollectionStatus,
        col_date,
        reason: str = None
        ) -> str:
    """ Create notification message with collection status,
    collection types, and instruction"""
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    waste_types = [col.waste_type.value for col in col_types]
    if "large_items" in waste_types:
        waste_types.remove("large_items")
        waste_types.append("large items")
    # back on schedule if collection date does not match tomorrow
    if col_date != tomorrow and col_status == CollectionStatus.on_schedule:
        resumed_message = f"NYC Sanitation Helper Reminder: Sanitation pickup will resume for tomorrow {tomorrow}! Have collection set out by midnight. "
        return resumed_message
    greeting = f"NYC Sanitation Helper: Sanitation pickup is {col_status.value.lower()} for tomorrow, {tomorrow.strftime('%m-%d-%Y')}. "
    if col_status == CollectionStatus.unknown:
        body = "There is currently no information about sanitation pickup."
    elif col_status == CollectionStatus.suspended:
        body = f"{reason} There will be no pickup, do not put any collection out."
    elif col_status == CollectionStatus.delayed:
        body = f"{reason} Put out all trash types."
    else:
        body = f"Have {", ".join(waste_types)} out for pickup by midnight."
    return greeting + body


def create_notifications():
    """ Create notification entries to be sent out to user"""
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")
    db = SessionLocal()
    collections = db.execute(select(Collection).join(
        Address, Collection.address_id == Address.id
    ).join(
        User, Address.user_id == User.id
    ).where(
        User.allow_notifications,
        or_(
            Collection.collection_date == tomorrow,
            and_(
                Collection.updated_collection_date == tomorrow,
                Collection.status == CollectionStatus.on_schedule
            )
        ))).scalars().all()
    for collection in collections:
        notification_exists = db.execute(
            select(Notification).where(
                Notification.collection_id == collection.id,
                Notification.collection_status == collection.status
            )).scalar_one_or_none()
        if notification_exists:
            continue
        new_notification = Notification(
            user_id=collection.address.user_id,
            collection_status=collection.status,
            message=create_notification_message(
                collection.collection_types,
                collection.status,
                collection.collection_date,
                collection.delay_reason,
            ),
            collection_id=collection.id
        )
        try:
            db.add(new_notification)
            db.commit()
        except IntegrityError:
            db.rollback()
    db.close()


def send_notifications():
    db = SessionLocal()
    notifications = db.execute(
        select(Notification).where(
            Notification.sent_at == None
        )).scalars().all()
    for notif in notifications:
        text_response = send_text(TextNotificationRequest(
            message=notif.message,
            user_phone_number=notif.user.phone_number
        ))
        db.execute(update(Notification).where(
            notif.id == Notification.id
        ).values(
            is_sent=text_response.is_sent,
            sent_at=text_response.sent_at
              ))
        db.commit()
    db.close()


def delete_notifications():
    """ Delete notifications older than 2 weeks"""
    db = SessionLocal()
    db.execute(delete(Notification).where(
            Notification.sent_at < datetime.today() - timedelta(days=14)
        )
    )
    db.commit()
    db.close()

def get_all_notifications():
    pass

def notification_job():
    """"""
    delete_notifications()
    create_notifications()
    send_notifications()


if __name__ == "__main__":
    create_notifications()

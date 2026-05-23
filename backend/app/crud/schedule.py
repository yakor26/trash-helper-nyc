from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase
from app.schemas.address import AddressCreate
from app.schemas.address import GeoclientAPIResponse
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleResponse


def get_schedule(db: Session, schedule: GeoclientAPIResponse) -> ScheduleResponse:
    sanitation_schedule = schedule.data.get("sanitation")
    schedule_exists = db.execute(select(Schedule).where(
        Schedule.days_trash == sanitation_schedule.get("days_trash"),
        Schedule.days_recycling == sanitation_schedule.get("days_recycling"),
        Schedule.days_compost == sanitation_schedule.get("days_compost"),
        Schedule.days_large_items == sanitation_schedule.get("days_large_items"))).scalar_one_or_none()
    return ScheduleResponse.model_validate(schedule_exists) if schedule_exists else None


def get_schedule_by_id(db: Session, schedule_id) -> ScheduleResponse:
    schedule = db.execute(select(Schedule).where(
        Schedule.id == schedule_id)).scalar_one_or_none()
    return ScheduleResponse.model_validate(schedule)


def create_schedule(db: Session, schedule: GeoclientAPIResponse) -> ScheduleResponse:
    """ Add sanitation schedule and return schedule"""
    sanitation_schedule = schedule.data.get("sanitation")
    # check if this schedule exists
    schedule_exists = get_schedule(db=db, schedule=schedule)
    # schedule already in db
    if schedule_exists:
        return None
    new_schedule = Schedule(**sanitation_schedule)
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return ScheduleResponse.model_validate(new_schedule)

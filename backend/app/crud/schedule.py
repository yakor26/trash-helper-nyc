from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase
from app.schemas.address import AddressCreate
from app.schemas.address import GeoclientAPIResponse
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleResponse, ScheduleBase


def get_schedule_by_day(db: Session, schedule: ScheduleBase) -> ScheduleResponse:
    schedule_exists = db.execute(select(Schedule).where(
        Schedule.days_trash == schedule.days_trash,
        Schedule.days_recycling == schedule.days_recycling,
        Schedule.days_compost == schedule.days_compost,
        Schedule.days_large_items == schedule.days_large_items)).scalar_one_or_none()
    return ScheduleResponse.model_validate(schedule_exists) if schedule_exists else None


def get_schedule_by_id(db: Session, schedule_id) -> ScheduleResponse:
    schedule = db.execute(select(Schedule).where(
        Schedule.id == schedule_id)).scalar_one_or_none()
    return ScheduleResponse.model_validate(schedule)


def create_schedule(db: Session, schedule: ScheduleBase) -> ScheduleResponse:
    """ Add sanitation schedule and return schedule"""
    # check if this schedule exists
    schedule_exists = get_schedule_by_day(db=db, schedule=schedule)
    # schedule already in db
    if schedule_exists:
        return None
    new_schedule = Schedule(**schedule.model_dump())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return ScheduleResponse.model_validate(new_schedule)


def delete_schedule(db: Session, schedule_id: int):
    """ Delete sanitation schedule """
    db.execute(delete(Schedule).where(Schedule.id == schedule_id))
    db.commit()

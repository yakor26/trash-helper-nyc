from typing import List
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    allow_notifications: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    locations: Mapped[List["Location"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"), nullable=False)
    location_type_id: Mapped[int] = mapped_column(ForeignKey("location_types.id"), nullable=False)
    street_address: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(5), nullable=False)
    user: Mapped["User"] = relationship(back_populates="locations")
    zone: Mapped["Zone"] = relationship(back_populates="locations")
    location_type: Mapped["LocationType"] = relationship(back_populates="locations")


class LocationType(Base):
    __tablename__ = "location_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    locations: Mapped[List["Location"]] = relationship(back_populates="location_types", cascade="all, delete-orphan")


class Zone(Base):
    __tablename__ = "zones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(50), nullable=False)
    locations: Mapped[List["Location"]] = relationship(back_populates="zone", cascade="all, delete-orphan")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="zone", cascade="all, delete-orphan")


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"), nullable=False)
    schedule_code: Mapped[str] = mapped_column(String(10), nullable=False)
    days: Mapped[str] = mapped_column(String(100), nullable=False)
    zone: Mapped["Zone"] = relationship(back_populates="schedules")
    # add specifics for type of waste picking up

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)



class ItemCategory(Base):
    __tablename__ = "item_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)


class Pickup(Base):
    __tablename__ = "pickups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())





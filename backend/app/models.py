from typing import List
from sqlalchemy.sql import func
from datetime import datetime, date
import enum
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, Table, Column, Enum, Date, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass

# fixed status
class CollectionStatus(enum.Enum):
    delayed = "DELAYED"
    on_schedule = "ON SCHEDULE"
    not_in_effect = "NOT IN EFFECT"
    suspended = "SUSPENDED"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
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
    locations: Mapped[List["Location"]] = relationship(back_populates="location_type")


class Zone(Base):
    __tablename__ = "zones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(50), nullable=False)
    locations: Mapped[List["Location"]] = relationship(back_populates="zone")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="zone", cascade="all, delete-orphan")


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"), nullable=False)
    days_trash: Mapped[JSON] = mapped_column(JSON, default=[])
    days_recycling: Mapped[JSON] = mapped_column(JSON, default=[])
    days_compost: Mapped[JSON] = mapped_column(JSON, default=[])
    days_large_items: Mapped[JSON] = mapped_column(JSON, default=[])
    zone: Mapped["Zone"] = relationship(back_populates="schedules")
    collections: Mapped[List["Collection"]] = relationship(back_populates="schedule")
    # add specifics for type of waste picking up


# junction table 
collections_collection_types = Table(
    "collections_collection_types",
    Base.metadata,
    Column("collection_id", ForeignKey("collections.id"), primary_key=True),
    Column("collection_type_id", ForeignKey("collection_types.id"), primary_key=True)
    )

class Collection(Base):
    __tablename__ = "collections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    schedule_id = mapped_column(Integer, ForeignKey("schedules.id"), nullable=False)
    collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[CollectionStatus] = mapped_column(Enum(CollectionStatus)) 
    schedule: Mapped["Schedule"] = relationship(back_populates="collections")
    collection_types: Mapped[List["CollectionType"]] = relationship(
        back_populates="collections",
        secondary=collections_collection_types)


class CollectionType(Base):
    __tablename__ = "collection_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    waste_type: Mapped[str] = mapped_column(String(50), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="collection_type")
    collections: Mapped[List["Collection"]] = relationship(
        back_populates="collection_types",
        secondary=collections_collection_types)

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_categories.id"), nullable=False)
    collection_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("collection_types.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(100), nullable=False)
    notes: Mapped[str] = mapped_column(String(200))
    collection_type: Mapped["CollectionType"] = relationship(back_populates="items")    
    item_category: Mapped["ItemCategory"] = relationship(back_populates="items")


class ItemCategory(Base):
    __tablename__ = "item_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="item_category")


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())





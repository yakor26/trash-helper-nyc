from typing import List
from datetime import date
import enum
from sqlalchemy import ForeignKey, Integer, Table, Column, Enum, Date, UniqueConstraint, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


# fixed status
class CollectionStatus(enum.Enum):
    delayed = "DELAYED"
    on_schedule = "ON SCHEDULE"
    not_in_effect = "NOT IN EFFECT"
    suspended = "SUSPENDED"
    unknown = "UNKNOWN"


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
    address_id = mapped_column(Integer, ForeignKey("addresses.id"), nullable=False)
    collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    updated_collection_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[CollectionStatus] = mapped_column(Enum(CollectionStatus), nullable=False)
    delay_reason: Mapped[str] = mapped_column(String(200), nullable=True)
    schedule: Mapped["Schedule"] = relationship(back_populates="collections")
    address: Mapped["Address"] = relationship(back_populates="collections")
    collection_types: Mapped[List["CollectionType"]] = relationship(
        back_populates="collections",
        secondary=collections_collection_types)
    __table_args__ = (UniqueConstraint("address_id", "updated_collection_date"),)

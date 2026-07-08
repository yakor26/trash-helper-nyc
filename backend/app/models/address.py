from typing import List
from sqlalchemy import String, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base
import enum


class AddressType(enum.Enum):
    residential = "residential"
    commercial = "commercial"
    mixed_use = "mixed-use"


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    address_type: Mapped[AddressType] = mapped_column(Enum(AddressType), nullable=False)
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"), nullable=False)
    street_address: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(50), default='NY')
    zip_code: Mapped[str] = mapped_column(String(5), nullable=False)
    user: Mapped["User"] = relationship(back_populates="addresses")
    schedule: Mapped["Schedule"] = relationship(back_populates="addresses")
    collections: Mapped[List["Collection"]] = relationship(back_populates="address", cascade="all, delete-orphan")

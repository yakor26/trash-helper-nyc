from typing import List
from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    days_trash: Mapped[list] = mapped_column(JSONB, default=[])
    days_recycling: Mapped[list] = mapped_column(JSONB, default=[])
    days_compost: Mapped[list] = mapped_column(JSONB, default=[])
    days_large_items: Mapped[list] = mapped_column(JSONB, default=[])
    collections: Mapped[List["Collection"]] = relationship(back_populates="schedule")
    addresses: Mapped[List["Address"]] = relationship(back_populates="schedule")
    __table_args__ = (
        UniqueConstraint("days_trash",
                         "days_recycling",
                         "days_compost",
                         "days_large_items"),)

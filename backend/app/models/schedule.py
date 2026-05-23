from typing import List
from sqlalchemy import Integer, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    days_trash: Mapped[JSON] = mapped_column(JSON, default=[])
    days_recycling: Mapped[JSON] = mapped_column(JSON, default=[])
    days_compost: Mapped[JSON] = mapped_column(JSON, default=[])
    days_large_items: Mapped[JSON] = mapped_column(JSON, default=[])
    collections: Mapped[List["Collection"]] = relationship(back_populates="schedule")
    addresses: Mapped[List["Address"]] = relationship(back_populates="schedule")
    # add specifics for type of waste picking up

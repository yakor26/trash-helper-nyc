from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from app.database import Base
import enum


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    collection_id: Mapped[int] = mapped_column(ForeignKey("collections.id"), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    user: Mapped["User"] = relationship(back_populates="notifications")
    collection: Mapped["Collection"] = relationship(back_populates="notifications")
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
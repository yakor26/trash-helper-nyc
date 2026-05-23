from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class ItemCategory(Base):
    __tablename__ = "item_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="item_category")

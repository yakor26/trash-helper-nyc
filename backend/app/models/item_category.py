from typing import List
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class ItemCategory(Base):
    __tablename__ = "item_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50), nullable=False)
    collection_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("collection_types.id"), nullable=False)
    disposal_instructions: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    accept_special_waste_site: Mapped[bool] = mapped_column(Boolean, default=False)
    accept_safe_disposal_site: Mapped[bool] = mapped_column(Boolean, default=False)
    items: Mapped[List["Item"]] = relationship(back_populates="item_category")
    collection_type: Mapped["CollectionType"] = relationship(back_populates="item_categories")
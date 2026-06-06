from typing import List
from app.models.collection import collections_collection_types
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base
import enum


class WasteType(enum.Enum):
    trash = "trash"
    recycling = "recycling"
    compost = "compost"
    large_items = "large_items"


class CollectionType(Base):
    __tablename__ = "collection_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    waste_type: Mapped[WasteType] = mapped_column(Enum(WasteType), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="collection_type")
    collections: Mapped[List["Collection"]] = relationship(
        back_populates="collection_types",
        secondary=collections_collection_types)

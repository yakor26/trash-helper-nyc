from typing import List
from app.models.collection import collections_collection_types
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class CollectionType(Base):
    __tablename__ = "collection_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    waste_type: Mapped[str] = mapped_column(String(50), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="collection_type")
    collections: Mapped[List["Collection"]] = relationship(
        back_populates="collection_types",
        secondary=collections_collection_types)

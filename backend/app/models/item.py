from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("item_categories.id"), nullable=False)
    collection_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("collection_types.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(100), nullable=False)
    notes: Mapped[str] = mapped_column(String(200))
    collection_type: Mapped["CollectionType"] = relationship(back_populates="items")    
    item_category: Mapped["ItemCategory"] = relationship(back_populates="items")

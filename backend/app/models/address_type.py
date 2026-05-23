from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class AddressType(Base):
    __tablename__ = "address_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    addresses: Mapped[List["Address"]] = relationship(back_populates="address_type")
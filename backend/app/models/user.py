from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import relationship, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[]
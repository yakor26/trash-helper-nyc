from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase, AddressCreate


def create_address(user_id: int, db: Session, address: AddressCreate) -> UserBase:
    """ Add an address for user """
    address_exists = db.execute(select(Address).where(
        Address.user_id == user_id,
        )
        )
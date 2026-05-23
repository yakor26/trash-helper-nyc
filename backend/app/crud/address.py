from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase
from app.schemas.address import AddressCreate
from app.schemas.address import GeoclientAPIResponse

def get_address(user_id: int, db: Session, address)

def create_address(user_id: int,
                   db: Session,
                   address: AddressCreate,
                   geoclient_data: GeoclientAPIResponse) -> UserBase:
    """ Add an address for user """
    address_data = geoclient_data.data.get("address")
    address_exists = db.execute(select(Address).where(
        Address.user_id == user_id,
        Address.address_type == address.address_type,
        Address.street_address == address_data.get("street_address"),
        Address.city == address_data.get("city"),
        Address.zip_code == address_data.get("zip_code")))
    db.add

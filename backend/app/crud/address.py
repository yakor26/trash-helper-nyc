from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase
from app.schemas.address import AddressCreate, AddressBase, AddressResponse
from app.schemas.address import GeoclientAPIResponse


def get_address_by_full_address(
        db: Session,
        address: AddressBase) -> AddressResponse:
    """Get address based on full user address"""
    address_response = db.execute(select(Address).where(
        Address.user_id == address.user_id,
        Address.address_type == address.address_type,
        Address.street_address == address.street_address,
        Address.city == address.city,
        Address.zip_code == address.zip_code)).scalar_one_or_none()
    if not address_response:
        return None
    return AddressResponse.model_validate(address_response)


def create_address(
        db: Session,
        address: AddressBase) -> AddressResponse:
    """ Add an address for user """
    new_address = Address(**address.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return AddressResponse.model_validate(new_address)

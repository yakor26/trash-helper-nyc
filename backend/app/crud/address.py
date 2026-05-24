from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserBase
from app.schemas.address import AddressUpdate, AddressBase, AddressResponse
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


def get_address_by_id(
        db: Session,
        user_id: int,
        address_id: int) -> AddressResponse:
    """ Get address based on address id"""
    address = db.execute(
        select(Address).where(
            Address.id == address_id,
            Address.user_id == user_id)).scalar_one_or_none()
    if not address:
        return None
    return AddressResponse.model_validate(address)


def get_all_addresses(db: Session, user_id: int) -> list:
    """ Get all addresses for user"""
    user_addresses = db.execute(
        select(Address).where(Address.user_id == user_id)).scalars().all()
    if len(user_addresses) == 0:
        return None
    return user_addresses


def create_address(
        db: Session,
        address: AddressBase) -> AddressResponse:
    """ Add an address for user """
    new_address = Address(**address.model_dump())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return AddressResponse.model_validate(new_address)


def delete_address(db: Session, user_id: int, address_id: int) -> None:
    """ Delete user address"""
    db.execute(
        delete(Address).where(
            Address.id == address_id,
            Address.user_id == user_id))
    db.commit()


def update_address_type(
        db: Session,
        user_id: int,
        address_id: int,
        update_addr: AddressUpdate) -> AddressResponse:
    """ Update user address"""
    # only change allowed is to user address type, since address already
    # validated by geoclient
    address = get_address_by_id(db=db, user_id=user_id, address_id=address_id)
    if not address:
        return None
    db.execute(
        update(Address).
        where(Address.user_id == user_id,
              Address.id == address_id).
        values(address_type=update_addr.address_type))
    db.commit()
    return get_address_by_id(db=db, user_id=user_id, address_id=address_id)

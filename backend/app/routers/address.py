from fastapi import APIRouter, HTTPException, status
from app.apis.geoclient import get_sanitation_info
from app.schemas.address import AddressCreate, AddressResponse, AddressBase, AddressUpdate
from app.schemas.schedule import ScheduleBase, ScheduleResponse
from app.dependencies import user_depend, db_depend
from app.crud.address import (
    create_address,
    get_address_by_full_address,
    delete_address,
    get_address_by_id,
    get_all_addresses,
    update_address_type)
from app.crud.schedule import (
    create_schedule,
    get_schedule_by_day,
    get_schedule_by_id)

router = APIRouter(prefix="/api/user", tags=["address"])


@router.get("/addresses")
def get_all_user_address(user: user_depend, db: db_depend):
    """ Get all current user addresses"""
    addresses = get_all_addresses(db=db, user_id=user.id)
    if not addresses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No addresses added yet")
    return addresses


@router.post("/addresses")
def set_address(address: AddressCreate, user: user_depend, db: db_depend) -> AddressResponse:
    """ Validate user address using geoclient api and create address and attach schedule"""
    response = get_sanitation_info(address.full_address)
    if response.status == "failed":
        raise HTTPException(status_code=response.error_code, detail=response.error_message)
    # print(response.data.get("sanitation"))
    # check schedule exists
    schedule = get_schedule_by_day(
        db=db,
        schedule=ScheduleBase(**response.data.get("sanitation"))
        )
    if not schedule:
        schedule = create_schedule(
            db=db,
            schedule=ScheduleBase(**response.data.get("sanitation"))
            )
    # check address already exists for user, return error
    address_exists = get_address_by_full_address(
        db=db,
        address=AddressBase(**response.data.get("address"),
                            schedule_id=schedule.id,
                            address_type=address.address_type,
                            user_id=user.id)
    )
    if address_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This address already exists")
    # create address if not
    new_address = create_address(
        db=db,
        address=AddressBase(**response.data.get("address"),
                            schedule_id=schedule.id,
                            address_type=address.address_type,
                            user_id=user.id)
    )
    return new_address


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_address(db: db_depend, user: user_depend, address_id: int):
    """ Delete user requested address """
    address_exists = get_address_by_id(db=db, user_id=user.id, address_id=address_id)
    if not address_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="address does not exist and cannot be deleted")
    delete_address(db=db, user_id=user.id, address_id=address_id)
    return {f"{address_id} has been successfully deleted"}


@router.patch("/addresses/{address_id}")
def update_user_address(
      db: db_depend,
      user: user_depend,
      update_addr: AddressUpdate,
      address_id: int) -> AddressResponse:
    address = update_address_type(
        db=db,
        user_id=user.id,
        address_id=address_id,
        update_addr=update_addr
      )
    if not address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="address does not exist and cannot be updated")
    return address


@router.get("/addresses/{address_id}")
def get_address(db: db_depend, user: user_depend, address_id: int) -> AddressResponse:
    address = get_address_by_id(db=db, user_id=user.id, address_id=address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="address does not exist"
        )
    return address


@router.get("/addresses/{address_id}/schedule")
def get_schedule_for_address(db: db_depend, user: user_depend, address_id: int) -> ScheduleResponse:
    """ Get sanitation collection schedule for address"""
    address = get_address_by_id(db=db, user_id=user.id, address_id=address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="address does not exist"
        )
    schedule = get_schedule_by_id(db=db, schedule_id=address.schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Schedule does not exist for this address"
        )
    return schedule

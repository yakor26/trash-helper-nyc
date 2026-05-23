from fastapi import APIRouter, HTTPException, status
from app.apis.geoclient import get_sanitation_info
from app.schemas.address import AddressCreate, GeoclientAPIResponse, AddressResponse, AddressBase
from app.dependencies import user_depend, db_depend
from app.crud.address import create_address, get_address_by_full_address
from app.crud.schedule import create_schedule, get_schedule

router = APIRouter(prefix="/api/address", tags=["address"])


@router.post("")
def get_address_schedule():
    return


@router.post("/address")
def set_address(address: AddressCreate, user: user_depend, db: db_depend) -> AddressResponse:
    response = get_sanitation_info(address.full_address)
    if response.status == "failed":
        raise HTTPException(status_code=response.error_code, detail=response.error_message)
    # check schedule exists
    schedule = get_schedule(db=db, schedule=response)
    if not schedule:
        schedule = create_schedule(db=db, schedule=response)
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

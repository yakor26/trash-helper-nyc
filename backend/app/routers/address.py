from fastapi import APIRouter, HTTPException
from app.apis.geoclient import get_sanitation_info
from app.schemas.address import AddressCreate, GeoclientAPIResponse
from app.schemas.user import UserUpdate, UserBase
from app.dependencies import user_depend, db_depend
from app.crud.address import create_address
from app.crud.schedule import create_schedule, get_schedule

router = APIRouter(prefix="api/address", tags=["address"])


@router.post("")
def get_address_schedule():
    return


@router.post("/address")
def set_address(address: AddressCreate, user: user_depend, db: db_depend) -> GeoclientAPIResponse:
    response = get_sanitation_info(address.full_address)
    if response.status == "failed":
        raise HTTPException(status_code=response.error_code, detail=response.error_message)
     # set schedule in db
    schedule = create_schedule(db=db, schedule=response)
    if not schedule:
        schedule = get_schedule(db=db, schedule=response)
    # set address in db
    address.schedule_id = schedule.id
    create_address(user_id=user.id, db=db, geoclient_data=response, address=address)

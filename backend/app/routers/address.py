from fastapi import APIRouter, HTTPException
from app.apis.geoclient import get_sanitation_info
from app.schemas.address import AddressCreate, GeoclientAPIResponse
from app.schemas.user import UserUpdate, UserBase
from app.dependencies import user_depend, db_depend

router = APIRouter(prefix="api/address", tags=["address"])


@router.post("")
def get_address_schedule():
   pass


@router.post("/address")
def set_address(address: AddressCreate, user: user_depend, db: db_depend) -> GeoclientAPIResponse:
      response = get_sanitation_info(address.full_address)
      if response.status == "failed":
          raise HTTPException(status_code=response.error_code, detail=response.error_message)
    
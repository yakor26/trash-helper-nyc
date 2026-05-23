from fastapi import APIRouter, HTTPException
from app.schemas.address import ScheduleRequest, ScheduleResponse
from app.apis.geoclient import get_sanitation_info

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/address")
def get_address_schedule(address_req: ScheduleRequest) -> ScheduleResponse:
    response = get_sanitation_info(address_req.full_address)
    if response.status == "failed":
        raise HTTPException(status_code=response.error_code, detail=response.error_message)
    return response

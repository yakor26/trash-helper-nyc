from fastapi import APIRouter

router = APIRouter(prefix="api/user", tags=["user"])


@router.post("")
def get_address_schedule():
   pass
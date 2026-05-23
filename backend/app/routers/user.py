from fastapi import APIRouter, HTTPException, status
from app.schemas.address import ScheduleRequest, GeoclientAPIResponse
from app.apis.geoclient import get_sanitation_info
from app.crud.user import update_user
from app.schemas.user import UserUpdate, UserBase
from app.dependencies import user_depend, db_depend

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/me")
def get_user(user: user_depend, db: db_depend) -> UserBase:
    """ Get current user info"""
    return user


@router.patch("/user")
def update_user_profile(db: db_depend, user: user_depend, update: UserUpdate) -> UserBase:
    """ Update user """
    user = update_user(db=db, user_id=user.id, user_update=update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update user")
    return user




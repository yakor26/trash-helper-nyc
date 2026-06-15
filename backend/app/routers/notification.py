from fastapi import APIRouter
from app.apis.text_notifications import send_text

router = APIRouter(prefix="/api/notifications", tags=["notification"])


@router.get("")
def get_notifications():
    """ Get all of user's notifications for 2 week period """
    pass
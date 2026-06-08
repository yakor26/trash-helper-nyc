from fastapi import APIRouter
from app.services.text_notifications import send_text

router = APIRouter(prefix="/api/notifications", tags=["notification"])


@router.post("/test")
def test_send_text():
    """ Testing sending texts to myself """
    return send_text()

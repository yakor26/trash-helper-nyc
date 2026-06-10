from fastapi import APIRouter
from app.apis.text_notifications import send_text

router = APIRouter(prefix="/api/notifications", tags=["notification"])


from pydantic import BaseModel
from datetime import datetime


class NotificationRequest(BaseModel):
    """ """
    user_id: int
    message: str
    sent_at: datetime | None = None


class NotificationResponse(NotificationRequest):
    """"""
    id: int

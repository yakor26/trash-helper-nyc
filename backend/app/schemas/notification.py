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


class TextNotificationRequest(BaseModel):
    """ Request sent to textbelt api"""
    message: str
    user_phone_number: str


class TextNotificationResponse(BaseModel):
    """ Response from textbelt api"""
    is_sent: bool = None
    error_code: int = None
    error_message: str = None
    sent_at: datetime = None

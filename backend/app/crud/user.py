from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserBase


def get_user_by_username(db: Session, username: str) -> UserBase:
    """ Get user from db"""
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user:
        return None
    return UserBase.model_validate(user)
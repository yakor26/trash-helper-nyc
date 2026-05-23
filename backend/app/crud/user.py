from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.schemas.user import UserBase, UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate, hashed_password):
    """ Create a new user"""
    # add user to db
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        phone_number=user.phone_number,
        allow_notifications=user.allow_notifications,
        addresses=[],
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> UserBase:
    """ Get user from db"""
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user:
        return None
    return UserBase.model_validate(user)


def get_user_by_id(db: Session, user_id: int) -> UserBase:
    """ Get user information based on user id"""
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none
    if not user:
        return None
    return UserBase.model_validate(user)


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserBase:
    """ Update user profile """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    update_fields = user_update.model_dump(exclude_none=True)
    db.execute(update(User).where(User.id == user_id).values(**update_fields))
    db.commit()
    db.refresh(user)
    return user

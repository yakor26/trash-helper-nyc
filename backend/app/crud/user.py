from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.models.user import User
from app.schemas.user import UserBase, UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError


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
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
    return UserBase.model_validate(new_user)


def get_user_by_username(db: Session, username: str) -> UserBase:
    """ Get user from db"""
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user:
        return None
    return UserBase.model_validate(user)


def check_user_by_email(db: Session, email: str, curr_user_id: int = None) -> bool:
    """ Return true/false if user email exists in db"""
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        return False
    if curr_user_id and user.id == curr_user_id:
        return False
    return True


def check_user_by_phone_num(db: Session, phone_num: str, curr_user_id: int = None) -> bool:
    """ Get user from db email"""
    user = db.execute(select(User).where(User.phone_number == phone_num)).scalar_one_or_none()
    if not user:
        return False
    if curr_user_id and user.id == curr_user_id:
        return False
    return True


def get_user_by_id(db: Session, user_id: int) -> UserBase:
    """ Get user information based on user id"""
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        return None
    return UserBase.model_validate(user)


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserBase:
    """ Update user profile """
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    update_fields = user_update.model_dump(exclude_none=True)
    try:
        db.execute(update(User).where(User.id == user_id).values(**update_fields))
        db.commit()
    except IntegrityError:
        db.rollback()
    return get_user_by_id(db, user_id)


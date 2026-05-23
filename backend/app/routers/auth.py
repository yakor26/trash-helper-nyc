from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm as oauth
from app.dependencies import user_depend, db_depend, get_cookie_auth
from app.schemas.user import UserCreate, UserBase
from app.auth.utils import get_user_by_username, set_tokens, oauth2_scheme, refresh_token_exceptions
from app.auth.utils import get_hashed_password, decode_token, credentials_exceptions, auth_user, create_token
from app.crud.user import get_user_by_username as crud_get_user
from app.models.user import User
from app.schemas.token import Token
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register_user(user: UserCreate, db: db_depend) -> Token:
    """ Register new user and provide tokens"""
    # confirm username not already exists
    user_exists = crud_get_user(db, user.username)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    hashed_password = get_hashed_password(user.password)
    # add user to db
    try:
        new_user = User(
            username=user.username,
            hashed_password=hashed_password,
            email=user.email,
            phone_number=user.phone_number,
            allow_notifications=user.get("allow_notifications", False),
            addresses=[],
        )
        db.add(new_user)
        db.commit()
    # for failed commit, rollback and raise error
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    # create tokens
    return set_tokens(user.username)


@router.post("/login")
def login_user(login_data: Annotated[oauth, Depends()], db: db_depend) -> Token:
    """ Login user and provide tokens"""
    # check user exists and authenticate
    user = auth_user(db, login_data.username, login_data.password)
    if not user:
        raise credentials_exceptions
    return set_tokens(user.username)


@router.post("/refresh")
def refresh_token(refresh_token: Annotated[str, Depends(get_cookie_auth)], db: db_depend) -> Token:
    """ Refresh access token"""
    if not refresh_token:
        raise refresh_token_exceptions
    # decode refresh token
    user_name = decode_token(refresh_token, token_type="refresh")
    if not user_name:
        raise refresh_token_exceptions
    # validate username returned
    user = crud_get_user(db, user_name)
    if not user:
        raise credentials_exceptions
    # new access token
    access_token = create_token(data={"sub": user.username}, token_type="access")
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
def get_user(user: user_depend, db: db_depend) -> UserBase:
    """ Get current user info"""
    return user

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm as oauth
from app.dependencies import user_depend, db_depend, get_cookie_auth
from app.schemas.user import UserCreate, UserBase
from app.auth.utils import get_user_by_username, set_tokens, oauth2_scheme, refresh_token_exceptions
from app.auth.utils import get_hashed_password, decode_token, credentials_exceptions, auth_user, create_token
from app.crud.user import (
    get_user_by_username as crud_get_user,
    create_user,
    check_user_by_email,
    check_user_by_phone_num)
from app.models.user import User
from app.schemas.token import Token
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register_user(user: UserCreate, db: db_depend) -> JSONResponse:
    """ Register new user and provide tokens"""
    # confirm username not already exists
    username_exists = crud_get_user(db, user.username)
    email_exists = check_user_by_email(db, user.email)
    phone_num_exists = check_user_by_phone_num(db, user.phone_number)
    if username_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if phone_num_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone Number already exists")
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists")

    hashed_password = get_hashed_password(user.password)
    user = create_user(db=db, user=user, hashed_password=hashed_password)
    return set_tokens(user.username)


@router.post("/login")
def login_user(login_data: Annotated[oauth, Depends()], db: db_depend) -> JSONResponse:
    """ Login user and provide tokens"""
    # check user exists and authenticate
    user = auth_user(db, login_data.username, login_data.password)
    if not user:
        raise credentials_exceptions
    return set_tokens(user.username)


@router.get("/refresh")
def refresh_token(refresh_token: Annotated[str, Depends(get_cookie_auth)], db: db_depend) -> Token:
    """ Refresh access token"""
    if not refresh_token:
        raise refresh_token_exceptions
    user_name = decode_token(refresh_token, token_type="refresh")
    if not user_name:
        raise refresh_token_exceptions
    user = crud_get_user(db, user_name)
    if not user:
        raise credentials_exceptions
    # new access token
    access_token = create_token(data={"sub": user.username}, token_type="access")
    return Token(access_token=access_token, token_type="bearer")

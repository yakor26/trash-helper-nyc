from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserInDB, UserBase
from app.schemas.token import Token
import jwt
import os
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

load_dotenv()
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
credentials_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
refresh_token_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token is missing or invalid",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_hashed_password(password: str) -> str:
    """ Hash and return user password """
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Validate user password"""
    return password_hasher.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str) -> UserInDB:
    """ Get user from db"""
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user:
        return None
    return UserInDB.model_validate(user)


def create_token(data: dict, token_type: str = "access") -> str:
    """ Create JWT access and refresh token """
    secret_key = ACCESS_SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY
    data_payload = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    if token_type == "refresh":
        expiration = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data_payload.update({"exp": expiration})
    jwt_token = jwt.encode(data_payload, secret_key, ALGORITHM)
    return jwt_token


def decode_token(token: str, token_type: str = "access"):
    """ Decode and validate tokens"""
    secret_key = ACCESS_SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY
    try:
        data_payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username = data_payload.get("sub")
        # no username in token
        if username is None:
            raise credentials_exceptions
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
    except InvalidTokenError:
        raise credentials_exceptions

    return username


def set_tokens(username: str) -> JSONResponse:
    """ generate access and refresh tokens"""
    access_token = create_token(data={"sub": username})
    refresh_token = create_token(data={"sub": username}, token_type="refresh")
    response = JSONResponse({"access_token": access_token, "username": username}, status_code=status.HTTP_200_OK)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
    # return access token and set refresh token in cookie
    return response


def auth_user(db: Session, username: str, password: str):
    """ Authenticate user and verify password"""
    # confirm user, use dummy password to prevent timing attacks
    user_db = get_user_by_username(db, username)
    if not user_db:
        verify_password(password, get_hashed_password("fakepassword"))
        return False
    # check password
    if not verify_password(password, user_db.hashed_password):
        return False
    return UserBase.model_validate(user_db)

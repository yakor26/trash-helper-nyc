from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User
from app.schemas.user import UserInDB, UserBase
import jwt
import os
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINS = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
credentials_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
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

def create_access_token(data: dict) -> str:
    """ Create JWT access token """
    data_payload = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    data_payload.update({"exp": expiration})
    jwt_token = jwt.encode(data_payload, SECRET_KEY, ALGORITHM)
    return jwt_token


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



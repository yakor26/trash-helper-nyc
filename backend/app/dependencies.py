from sqlmodel import Session
from fastapi import Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from app.database import SessionLocal
from typing import Annotated
from app.schemas.user import UserBase
from app.auth.utils import oauth2_scheme, credentials_exceptions, decode_token, get_user_by_username



def get_db():
    """ Dependency for db session"""
    with SessionLocal() as db:
        yield db

def get_cookie_auth(request: Request):
    """ Check cookie for refresh token"""
    refresh_token= request.cookies.get("refresh_token")
    if not refresh_token:
        return None
    return refresh_token


def get_curr_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> UserBase:
    """ Dependency to get current user based on token"""
    username = decode_token(token)
    # decode token will raise exception if invalid
    db_user = get_user_by_username(db, username)
    # user not found
    if not db_user:
        raise credentials_exceptions
    # validate user and return public user info
    user = UserBase.model_validate(db_user)
    return user
    
    
db_depend = Annotated[Session, Depends(get_db)]
user_depend = Annotated[UserBase, Depends(get_curr_user)]


        


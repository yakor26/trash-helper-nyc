from sqlmodel import Session
from fastapi import Depends
from app.database import SessionLocal
from typing import Annotated
from app.auth.utils import oauth2_scheme



def get_db():
    """ Dependency for db session"""
    with SessionLocal() as db:
        yield db

def get_curr_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """ Dependency to get current user based on token"""



db_depend = Annotated[Session, Depends(get_db)]


        


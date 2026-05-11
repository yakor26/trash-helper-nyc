from sqlmodel import Session
from fastapi import Depends
from app.database import SessionLocal
from typing import Annotated



def get_session():
    with SessionLocal() as session:
        yield session

db_depend = Annotated[Session, Depends(get_session)]


        


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# set check same thread to false to allow for use in same db in diff threads
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(engine)


from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models import Base

# on startup
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(bind=engine)




app = FastAPI(title="NYC Waste Helper", lifespan=lifespan)
@app.get("/")
def root():
    return "Placeholder for root"
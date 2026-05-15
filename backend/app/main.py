from fastapi import FastAPI
from app.routers.user import router as user_router
from contextlib import asynccontextmanager
from app.database import engine
from app.models import Base

# on startup
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(bind=engine)




app = FastAPI(title="NYC Waste Helper")
app.include_router(user_router)

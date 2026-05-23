from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user import router as user_router
from app.routers.collection import router as collection_router
from app.routers.auth import router as auth_router
from contextlib import asynccontextmanager
from app.database import engine

# on startup
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     Base.metadata.create_all(bind=engine)


app = FastAPI(title="NYC Waste Helper")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(collection_router)

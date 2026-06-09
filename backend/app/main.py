from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user import router as user_router
from app.routers.collection import router as collection_router
from app.routers.auth import router as auth_router
from app.routers.address import router as address_router
from app.routers.notification import router as notification_router
from contextlib import asynccontextmanager
from app.database import engine
from apscheduler.schedulers.background import BackgroundScheduler
from app.crud.collection import create_collection_event

# on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_collection_event)

    # Base.metadata.create_all(bind=engine)


app = FastAPI(title="NYC Waste Helper")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(address_router)
app.include_router(collection_router)
app.include_router(notification_router)

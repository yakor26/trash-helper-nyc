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
from app.crud.collection import collection_job
from app.crud.notification import notification_job
from datetime import datetime, timedelta


# on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(collection_job, "cron", hour=16, next_run_time=datetime.now())
    scheduler.add_job(notification_job, "cron", hour=18, next_run_time=datetime.now() + timedelta(minutes=3))
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="NYC Waste Helper", lifespan=lifespan)
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

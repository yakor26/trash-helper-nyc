from fastapi import APIRouter


router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
def register_user():
    return {"temp": "register"}

@router.post("/login")
def login_user():
    
    return {"temp": "login"}

@router.get("/me")
def get_user():
    return {"temp": "user info"}


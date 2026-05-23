from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
import string
from datetime import datetime
from app.schemas.address import AddressResponse


# user authentication
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=2)
    last_name: str | None = None
    email: EmailStr
    phone_number: PhoneNumber
    allow_notifications: bool = False
    password: str = Field(min_length=12, max_length=100)
    confirm_password: str = Field(min_length=12, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password):
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        if not any(char in string.punctuation for char in password):
            raise ValueError("Password must contain at least one special character")
        return password

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, confirm_password, info):
        if info.data.get("password") is None:
            raise ValueError("Password not provided")
        if confirm_password != info.data.get("password"):
            raise ValueError("Passwords do not match")
        return confirm_password


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2)
    last_name: str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    allow_notifications: bool | None = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: PhoneNumber
    allow_notifications: bool
    addresses: list[AddressResponse] = []
    # set to allow create pydantic model from queries
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

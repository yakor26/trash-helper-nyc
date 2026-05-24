from pydantic import BaseModel, Field, ConfigDict
from app.models.address import AddressType


class AddressCreate(BaseModel):
    full_address: str = Field(min_length=2, max_length=300)
    address_type: AddressType


class AddressUpdate(BaseModel):
    address_type: AddressType


class AddressBase(BaseModel):
    user_id: int
    address_type: AddressType
    schedule_id: int
    street_address: str
    city: str
    zip_code: str

    model_config = ConfigDict(from_attributes=True)


class AddressResponse(AddressBase):
    id: int


class GeoclientAPIResponse(BaseModel):
    status: str
    error_code: int | None = None
    error_message: str | None = None
    data: dict = {}

from pydantic import BaseModel, Field, field_validator
from app.models.address import AddressType


class AddressCreate(BaseModel):
    full_address: str = Field(min_length=2, max_length=300)
    address_type: AddressType


class AddressResponse(BaseModel):
    id: int
    address_type: AddressType
    schedule_id: int
    street_address: str
    city: str
    zip_code: str




class ScheduleRequest(BaseModel):
    full_address: str = Field(min_length=3, max_length=300)
    # state: str = "NY"
    # city: str = Field(min_length=2, max_length=100)
    # zipcode: str

    # @field_validator("user_zipcode")
    # def valid_zipcode(cls, zipcode):
    #     if len(zipcode) < 5 or not any(char.isdigit() for char in zipcode):
    #         raise ValueError("Invalid Zipcode")
        

class GeoclientAPIResponse(BaseModel):
    status: str
    error_code: int | None = None
    error_message: str | None = None
    data: dict = {}

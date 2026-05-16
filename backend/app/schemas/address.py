from pydantic import BaseModel, Field, field_validator

class ScheduleRequest(BaseModel):
    full_address: str = Field(min_length=3, max_length=300)
    # state: str = "NY"
    # city: str = Field(min_length=2, max_length=100)
    # zipcode: str

    # @field_validator("user_zipcode")
    # def valid_zipcode(cls, zipcode):
    #     if len(zipcode) < 5 or not any(char.isdigit() for char in zipcode):
    #         raise ValueError("Invalid Zipcode")
        

class ScheduleResponse(BaseModel):
    status: str
    error_code: int | None = None
    error_message: str | None = None
    data: dict = {}
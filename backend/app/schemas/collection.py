from pydantic import BaseModel, Field

# for calls to 311 api, get collection status
class CollectionStatusRequest(BaseModel):
    from_date: str = Field(min_length=10, max_length=10)
    to_date: str = Field(min_length=10, max_length=10)

class CollectionStatusResponse(BaseModel):
    status: str
    error_code: int = None
    error_message: str = None
    data: list = []

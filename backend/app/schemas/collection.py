from pydantic import BaseModel, Field
from datetime import datetime


# for calls to 311 api, get collection status
class CollectionStatusRequest(BaseModel):
    # from_date: str = datetime.today().strftime("%m/%d/%Y")
    # to_date: str = datetime.today().strftime("%m/%d/%Y")
    from_date: str = "05/25/26"
    to_date: str = "05/25/26"


class CollectionStatusResponse(BaseModel):
    status: str
    error_code: int = None
    error_message: str = None
    data: list = []

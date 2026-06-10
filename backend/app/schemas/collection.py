from pydantic import BaseModel, Field
from datetime import datetime
from app.models.collection_type import WasteType, CollectionType
from app.schemas.address import AddressResponse


# for calls to 311 api, get collection status
class CollectionStatusRequest(BaseModel):
    """ Request for collection status submitted to api"""
    from_date: str = datetime.today().strftime("%m/%d/%Y")
    to_date: str = datetime.today().strftime("%m/%d/%Y")
    # holiday example
    # from_date: str = "05/25/26"
    # to_date: str = "05/25/26"


class CollectionStatusResponse(BaseModel):
    """ Response for collection status request from api """
    status: str
    error_code: int = None
    error_message: str = None
    data: list = []


class CollectionAddressResponse(AddressResponse):
    """ info for address collection type"""
    collection_types: list[WasteType] = []


class CollectionsAllRequest(BaseModel):
    """ Store info for address with collections for next day"""
    address_data: list[CollectionAddressResponse] = []

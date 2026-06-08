from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse
from app.apis.nyc_311 import get_collection_status

router = APIRouter(prefix="/api/collections", tags=["collection"])


@router.get("/status")
def collection_status(specific_date: datetime = None) -> CollectionStatusResponse:
    """ Get nyc sanitation collection status for specific date, defaults to today"""
    if specific_date:
        date_request = CollectionStatusRequest(
            from_date=specific_date.strftime("%m/%d/%Y"),
            to_date=specific_date.strftime("%m/%d/%Y")
            )
        print(date_request)
    else:
        date_request = CollectionStatusRequest()
    status_response = get_collection_status(date_request)
    if status_response.status == "failed":
        raise HTTPException(status_code=status_response.error_code or 500, detail=status_response.error_message)
    return status_response

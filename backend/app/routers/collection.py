from fastapi import APIRouter, HTTPException
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse
from app.apis.nyc_311 import get_collection_status

router = APIRouter(prefix="/api/collection", tags=["collection"])


@router.post("/status")
def collection_status(date_request: CollectionStatusRequest) -> CollectionStatusResponse:
    """ Get nyc sanitation collection status for a date"""
    status_response = get_collection_status(date_request)
    if status_response.status == "failed":
        raise HTTPException(status_code=status_response.error_code or 500, detail=status_response.error_message)
    return status_response
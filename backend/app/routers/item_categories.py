from fastapi import APIRouter


router = APIRouter(prefix="/api/item-categories", tags=["item-categories"])

@router.get("")
def get_item_categories():
    """"""
    pass
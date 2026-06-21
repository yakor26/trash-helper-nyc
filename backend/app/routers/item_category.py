from fastapi import APIRouter
from app.schemas.item_category import ItemCategorySearch, SearchResult
from app.services.search_service import combined_search


router = APIRouter(prefix="/api/item-categories", tags=["item-categories"])


@router.get("")
def get_item_category(search: str) -> SearchResult:
    """ Return closest matching category and disposal instructions using
    search service based on user item search query."""
    result = combined_search(ItemCategorySearch(search_value=search))
    return result

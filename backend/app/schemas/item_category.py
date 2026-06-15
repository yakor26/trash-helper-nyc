from pydantic import BaseModel, Field, ConfigDict
from app.models.collection_type import CollectionType


class ItemCategorySearch(BaseModel):
    search_value: str = Field(min_length=2, max_length=100)


class ItemCategoryResult(BaseModel):
    category_name: str
    # collection_type: str = CollectionType
    disposal_instructions: str
    accept_special_waste_site: bool
    accept_safe_disposal_site: bool

    model_config = ConfigDict(from_attributes=True)


class SearchResult(BaseModel):
    results_count: int = 0
    data: list[ItemCategoryResult]
    error_code: int = None
    error_message: str = None

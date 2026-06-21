from pydantic import BaseModel, Field, ConfigDict


class ItemCategorySearch(BaseModel):
    search_value: str = Field(min_length=2, max_length=100)


class ItemCategoryResult(BaseModel):
    id: int
    category_name: str
    col_type: str = ""
    disposal_instructions: str
    accept_special_waste_site: bool
    accept_safe_disposal_site: bool

    model_config = ConfigDict(from_attributes=True)


class SearchResult(BaseModel):
    results_count: int = 0
    data: list[ItemCategoryResult] = None
    error_message: str = None

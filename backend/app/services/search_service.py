from app.services.auto_correct import spell_correct
from sqlalchemy import select
from app.database import SessionLocal
from app.models.item_category import ItemCategory
from app.schemas.item_category import ItemCategoryResult, ItemCategorySearch, SearchResult


def basic_search(search: ItemCategorySearch):
    search_entry = spell_correct(search.search_value)
    # print(search_entry)
    db = SessionLocal()
    result = db.execute(
        select(ItemCategory).where(
            ItemCategory.description.match(
                search_entry))).scalars().all()
    result_list = [ItemCategoryResult.model_validate(cat) for cat in result]
    print(result_list)



def main():
    test_input = input("How to dispose of: ")
    basic_search(ItemCategorySearch(search_value=test_input))


if __name__ == "__main__":
    main()
from app.services.auto_correct import spell_correct
from sqlalchemy import select
from app.database import SessionLocal
from app.models.item_category import ItemCategory
from app.schemas.item_category import ItemCategoryResult, ItemCategorySearch, SearchResult
import torch
from sentence_transformers import SentenceTransformer

# pretrained model
# embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embedder = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
db = SessionLocal()
descriptions_query = db.execute(
    select(ItemCategory)).scalars().all()
descriptions = [cat.description for cat in descriptions_query]
descriptions_embedded = embedder.encode_document(descriptions, convert_to_tensor=True)


def basic_search(search: ItemCategorySearch):
    search_entry = spell_correct(search.search_value)
    # print(search_entry)
    db = SessionLocal()
    result = db.execute(
        select(ItemCategory).where(
            ItemCategory.description.match(
                search_entry))).scalars().all()
    result_list = [ItemCategoryResult.model_validate(cat) for cat in result]
    # print(result_list)
    db.close()


def vector_search(search: ItemCategorySearch):
    search_keyword = spell_correct(search.search_value)
    search_query = f"What matches category of {search_keyword}?"
    # search_query = f"search_query: {search_keyword}"

    embedded_search = embedder.encode_query(search_query, convert_to_tensor=True)
    similarity_scores = embedder.similarity(embedded_search, descriptions_embedded)[0]
    scores, idxs = torch.topk(similarity_scores, 5)
    for s, i in zip(scores, idxs):
        print(f"Score: {s:.2f}", descriptions[i])


def main():
    test_input = input("How to dispose of: ")
    # basic_search(ItemCategorySearch(search_value=test_input))
    vector_search(ItemCategorySearch(search_value=test_input))


if __name__ == "__main__":
    main()
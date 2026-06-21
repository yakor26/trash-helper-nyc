from app.services.auto_correct import spell_correct
from sqlalchemy import select
from app.database import SessionLocal
from app.models.item_category import ItemCategory
from app.models.collection_type import CollectionType
from app.schemas.item_category import ItemCategoryResult, ItemCategorySearch, SearchResult
import torch
from sentence_transformers import SentenceTransformer


db = SessionLocal()
descriptions_query = db.execute(
    select(ItemCategory)).scalars().all()
descriptions = [cat.description for cat in descriptions_query]
category_names = [cat.category_name for cat in descriptions_query]
embedder = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5")
descriptions_embedded = embedder.encode_document(descriptions, convert_to_tensor=True)


def assign_ranking_score(rank) -> float:
    """ Assign score for results from each search"""
    score = 1 / (rank + 61)
    return score


def get_combined_scores(k_results, v_results) -> dict:
    """ Format total ranking for results from both searches """
    if not k_results and v_results:
        return {}
    if not k_results:
        return v_results
    if not v_results:
        return k_results
    combo = k_results
    for k, v in v_results.items():
        if k in combo:
            combo[k] += v
        else:
            combo[k] = v
    sorted_combo = {k: v for k, v in sorted(combo.items(), key=lambda x: x[1], reverse=True)}
    return sorted_combo


def keyword_search(search: ItemCategorySearch) -> dict:
    """ Keyword search matching against description in db for categories"""
    search_entry = spell_correct(search.search_value)
    result = db.execute(
        select(ItemCategory).where(
            ItemCategory.description.match(
                search_entry))).scalars().all()
    result_list = [ItemCategoryResult.model_validate(cat) for cat in result]
    keyword_scores = {c.category_name: assign_ranking_score(i) for i, c in enumerate(result_list)}
    db.close()
    return keyword_scores


def vector_search(search: ItemCategorySearch) -> dict:
    """ Use embedding model to for sentence similarity in
    descriptions to search query
    """
    search_keyword = spell_correct(search.search_value)
    search_query = f"search_query: What category does {search_keyword} belong in"
    embedded_search = embedder.encode_query(search_query, convert_to_tensor=True)
    similarity_scores = embedder.similarity(embedded_search, descriptions_embedded)[0]
    scores, idxs = torch.topk(similarity_scores, 5)
    semantic_scores = {category_names[i]: assign_ranking_score(p) for p, i in enumerate(idxs)}
    return semantic_scores


def combined_search(search: ItemCategorySearch) -> SearchResult:
    """ Merge results from keyword search and semantic search.
    Rank using RRF and return highest ranked score
    """
    keyword_scores = keyword_search(search)
    vector_scores = vector_search(search)
    combined_rankings = get_combined_scores(keyword_scores, vector_scores)
    if combined_rankings == {}:
        return SearchResult(
            error_message="Unable to find proper disposal instructions for this item"
            )
    highest_rank = max(combined_rankings, key=lambda x: combined_rankings[x])
    highest_rank_category = db.execute(
        select(ItemCategory).join(
            CollectionType, ItemCategory.collection_type_id == CollectionType.id
        ).where(
            ItemCategory.category_name == highest_rank)
            ).scalar_one_or_none()
    if not highest_rank_category:
        return SearchResult(
            error_message="Unable to find proper disposal instructions for this item"
            )
    data = ItemCategoryResult.model_validate(highest_rank_category)
    data.col_type = highest_rank_category.collection_type.waste_type.value
    return SearchResult(
        results_count=1,
        data=[data]
    )


def main():
    print(combined_search(ItemCategorySearch(search_value="ne")))


if __name__ == "__main__":
    main()

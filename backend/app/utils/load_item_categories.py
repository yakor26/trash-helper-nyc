import pandas as pd
from pathlib import Path
from app.database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app.models.collection_type import CollectionType

directory = Path(__file__).parent


def load_item_categories():
    item_categories_df = pd.read_csv(f"{directory}/NYCItemCategoriesV3.csv")
    db = SessionLocal()
    col_types = db.execute(select(CollectionType)).scalars().all()
    col_type_map = {col.waste_type.value: col.id for col in col_types}
    # create collection_type_id col
    item_categories_df["collection_type_id"] = item_categories_df["collection_type"].map(col_type_map)
    item_categories_df.drop(columns="collection_type", inplace=True)
    print(item_categories_df.head())
    try:
        with engine.connect() as connection:
            with connection.begin():
                item_categories_df.to_sql(
                    "item_categories",
                    con=engine,
                    if_exists="append",
                    index=False
                )
        print("Loaded Item Categories")
    except SQLAlchemyError as e:
        print(f"Error loading Item Categories: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    load_item_categories()

import pandas as pd
from pathlib import Path
from app.database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError

directory = Path(__file__).parent


def load_item_categories():
    item_categories_df = pd.read_csv(f"{directory}/NYCItemCategoriesV3.csv")
    print(item_categories_df.head())
    print(item_categories_df.shape)
    print(item_categories_df.dtypes)
    db = SessionLocal()
    
    try:
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


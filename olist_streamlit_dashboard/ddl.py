"""
ddl.py

"""

from __future__ import annotations

from pathlib import Path
import duckdb


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "my.db"
SOURCE_DIR = BASE_DIR / "source"
QUERIES_DIR = BASE_DIR / "queries"



def _read_sql(path: Path) -> str:
    """Read a .sql file as text."""
    return path.read_text(encoding="utf-8")


def load_csv_to_table(con: duckdb.DuckDBPyConnection, csv_path: Path, table_name: str) -> None:
    
    con.execute(
        f"""
        INSERT INTO {table_name}
        SELECT * FROM read_csv_auto(?, header=True)
        """,
        [str(csv_path)],
    )


def build_db() -> None:
    
    con = duckdb.connect(str(DB_PATH))

    # 1) Create tables
    con.execute(_read_sql(QUERIES_DIR / "01_create_tables.sql"))

    # 2) Load data
    mapping = {
        "olist_customers_dataset.csv": "customers",
        "olist_orders_dataset.csv": "orders",
        "olist_order_items_dataset.csv": "order_items",
        "olist_products_dataset.csv": "products",
        "olist_order_payments_dataset.csv": "payments",
        "olist_order_reviews_dataset.csv": "reviews",
    }

    for filename, table in mapping.items():
        path = SOURCE_DIR / filename
        if path.exists():
            load_csv_to_table(con, path, table)

    # 3) Create views
    con.execute(_read_sql(QUERIES_DIR / "02_create_views.sql"))

    con.close()
    print("✅ DuckDB database built: my.db")


if __name__ == "__main__":
    build_db()

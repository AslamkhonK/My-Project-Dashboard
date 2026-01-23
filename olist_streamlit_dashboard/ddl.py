"""
ddl.py

Creates DuckDB tables and loads data from CSV files in /source.
Also creates SQL views required for analytics.
"""

from __future__ import annotations

from pathlib import Path
import duckdb


DB_PATH = Path("my.db")
SOURCE_DIR = Path("source")
QUERIES_DIR = Path("queries")


def _read_sql(path: Path) -> str:
    """Read a .sql file as text."""
    return path.read_text(encoding="utf-8")


def load_csv_to_table(con: duckdb.DuckDBPyConnection, csv_path: Path, table_name: str) -> None:
    """
    Load a CSV file into an existing DuckDB table.

    Args:
        con: DuckDB connection.
        csv_path: Path to CSV file.
        table_name: Name of the target table.
    """
    con.execute(
        f"""
        INSERT INTO {table_name}
        SELECT * FROM read_csv_auto(?, header=True)
        """,
        [str(csv_path)],
    )


def build_db() -> None:
    """
    Build local DuckDB database:
    1) Create empty tables from SQL
    2) Load CSV data into tables
    3) Create analytic views
    """
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

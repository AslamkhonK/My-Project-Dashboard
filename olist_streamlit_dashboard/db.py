"""
db.py
"""

from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd


DB_PATH = Path("my.db")
SQL_PATH = Path("queries/03_queries.sql")


def _load_named_queries(sql_text: str) -> dict[str, str]:
    
    
    queries: dict[str, str] = {}
    current_name = None
    current_lines: list[str] = []

    for line in sql_text.splitlines():
        if line.strip().lower().startswith("-- name:"):
            # flush previous
            if current_name and current_lines:
                queries[current_name] = "\n".join(current_lines).strip()
            current_name = line.split(":", 1)[1].strip()
            current_lines = []
        else:
            if current_name is not None:
                current_lines.append(line)

    if current_name and current_lines:
        queries[current_name] = "\n".join(current_lines).strip()

    return queries


_QUERIES = _load_named_queries(SQL_PATH.read_text(encoding="utf-8"))


def query_df(query_name: str, params: list) -> pd.DataFrame:

    sql = _QUERIES[query_name]
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        return con.execute(sql, params).fetchdf()

"""
main.py

Streamlit dashboard using DuckDB + Pandas + Plotly.
"""

from __future__ import annotations

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

from db import query_df


st.set_page_config(page_title="Olist Sales Dashboard", layout="wide")

st.title("📦 Olist E-commerce Dashboard")
st.caption("Интерактивный дашборд на DuckDB + Streamlit + Plotly. Данные: Olist (Brazil).")

# --- Helpers
def to_dt(x: pd.Timestamp) -> datetime:
    """Convert pandas timestamp to Python datetime."""
    return pd.to_datetime(x).to_pydatetime()


# --- Load min/max dates for filters (через запрос)
# Берём диапазон из vw_monthly_revenue (не читаем CSV напрямую)
df_months = query_df("monthly_revenue", [datetime(2016, 1, 1), datetime(2020, 12, 31)])
if df_months.empty:
    st.error("База пустая. Сначала запусти: python ddl.py")
    st.stop()

min_month = to_dt(df_months["month"].min())
max_month = to_dt(df_months["month"].max())

# --- Sidebar filters (2+ элемента управления)
st.sidebar.header("Фильтры")

date_range = st.sidebar.date_input(
    "Диапазон дат (по месяцам)",
    value=(min_month.date(), max_month.date()),
    min_value=min_month.date(),
    max_value=max_month.date(),
)

category = st.sidebar.text_input(
    "Категория (точное значение, опционально)",
    value="",
    help="Оставь пустым, чтобы показать все категории. Пример: beleza_saude",
).strip().lower()

cat_param = category if category else None

start_dt = datetime.combine(date_range[0], datetime.min.time())
end_dt = datetime.combine(date_range[1], datetime.max.time())

# --- Queries
df_rev = query_df("monthly_revenue", [start_dt, end_dt])
df_cat = query_df("category_revenue", [start_dt, end_dt, cat_param, cat_param])
df_status = query_df("status_share", [start_dt, end_dt, cat_param, cat_param])
df_deliv = query_df("delivery_vs_rating", [start_dt, end_dt, cat_param, cat_param])
df_states = query_df("top_states", [start_dt, end_dt, cat_param, cat_param])

# --- Layout
c1, c2 = st.columns(2)
with c1:
    st.subheader("1) Выручка по месяцам")
    fig1 = px.line(df_rev, x="month", y="revenue", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("2) Топ категорий по выручке (Top 20)")
    fig2 = px.bar(df_cat, x="revenue", y="product_category", orientation="h")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader("3) Доля статусов заказов")
    fig3 = px.pie(df_status, names="order_status", values="orders_cnt")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("4) Среднее время доставки vs рейтинг")
    fig4 = px.bar(df_deliv, x="review_score", y="avg_delivery_days")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("5) Топ штатов по выручке")
fig5 = px.bar(df_states, x="customer_state", y="revenue")
st.plotly_chart(fig5, use_container_width=True)

st.info("Если графики пустые — попробуй расширить диапазон дат или очистить фильтр категории.")

# Olist Streamlit Dashboard

Интерактивный дашборд продаж на базе DuckDB + Streamlit + Plotly.  
Автор: <Aslamkhon Kaniev> (GitHub: <https://github.com/AslamkhonK/My-Project-Dashboard>)
Streamlit link <https://my-project-dashboard-fknf3fycisd4dqerlc223l.streamlit.app/>

## Описание датасета
Используется публичный датасет Olist Brazilian E-Commerce (Kaggle). 
Данные представлены в нескольких таблицах (orders, order_items, products, customers, payments, reviews).

## Структура репозитория
- source/ — CSV файлы датасета
- queries/ — SQL (DDL таблиц, вьюшки, запросы)
- ddl.py — создание таблиц + загрузка данных + создание вьюшек
- db.py — получение данных из DuckDB (только через SQL)
- main.py — Streamlit приложение (дашборд)
- my.db — локальная база DuckDB
ssh-keygen -t ed25519 -C "aslamkhonk@gmail.com"

## Инструменты
- DuckDB — хранение/запросы
- Pandas — DataFrame
- Plotly — визуализации
- Streamlit — UI/дашборд

## Запуск локально
1) Установить зависимости:
```bash
pip install -r requirements.txt

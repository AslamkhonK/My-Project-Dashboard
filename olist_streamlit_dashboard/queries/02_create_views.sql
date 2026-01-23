-- 02_create_views.sql

DROP VIEW IF EXISTS vw_sales_fact;
DROP VIEW IF EXISTS vw_monthly_revenue;
DROP VIEW IF EXISTS vw_top_categories;
DROP VIEW IF EXISTS vw_delivery_vs_rating;

-- Факт продаж (JOIN + даты + текст)
CREATE VIEW vw_sales_fact AS
SELECT
  o.order_id,
  o.customer_id,
  c.customer_state,
  c.customer_city,
  o.order_status,
  o.order_purchase_timestamp,
  i.product_id,
  LOWER(COALESCE(p.product_category_name, 'unknown')) AS product_category,
  i.price,
  i.freight_value,
  COALESCE(pay.payment_value, i.price + i.freight_value) AS payment_value,
  r.review_score,
  o.order_delivered_customer_date,
  o.order_estimated_delivery_date
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
LEFT JOIN products p ON p.product_id = i.product_id
LEFT JOIN (
  SELECT order_id, SUM(payment_value) AS payment_value
  FROM payments
  GROUP BY order_id
) pay ON pay.order_id = o.order_id
LEFT JOIN reviews r ON r.order_id = o.order_id;

-- Выручка по месяцам (агрегации + date_trunc)
CREATE VIEW vw_monthly_revenue AS
SELECT
  DATE_TRUNC('month', order_purchase_timestamp) AS month,
  SUM(payment_value) AS revenue,
  COUNT(DISTINCT order_id) AS orders_cnt,
  AVG(payment_value) AS avg_order_value
FROM vw_sales_fact
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- Топ категорий по выручке с оконной функцией (RANK)
CREATE VIEW vw_top_categories AS
SELECT
  product_category,
  SUM(payment_value) AS revenue,
  COUNT(DISTINCT order_id) AS orders_cnt,
  RANK() OVER (ORDER BY SUM(payment_value) DESC) AS revenue_rank
FROM vw_sales_fact
GROUP BY 1;

-- Доставка vs рейтинг (datediff + агрегации)
CREATE VIEW vw_delivery_vs_rating AS
SELECT
  product_category,
  review_score,
  AVG(
    DATE_DIFF('day', order_purchase_timestamp, order_delivered_customer_date)
  ) AS avg_delivery_days,
  COUNT(*) AS rows_cnt
FROM vw_sales_fact
WHERE order_delivered_customer_date IS NOT NULL
  AND order_purchase_timestamp IS NOT NULL
  AND review_score IS NOT NULL
GROUP BY 1, 2;

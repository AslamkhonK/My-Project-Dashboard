-- 03_queries.sql

-- name: monthly_revenue
SELECT * FROM vw_monthly_revenue
WHERE month BETWEEN ? AND ?
ORDER BY month;

-- name: category_revenue
SELECT
  product_category,
  SUM(payment_value) AS revenue
FROM vw_sales_fact
WHERE order_purchase_timestamp BETWEEN ? AND ?
  AND (? IS NULL OR product_category = ?)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 20;

-- name: status_share
SELECT
  order_status,
  COUNT(DISTINCT order_id) AS orders_cnt
FROM vw_sales_fact
WHERE order_purchase_timestamp BETWEEN ? AND ?
  AND (? IS NULL OR product_category = ?)
GROUP BY 1
ORDER BY orders_cnt DESC;

-- name: delivery_vs_rating
SELECT
  review_score,
  AVG(DATE_DIFF('day', order_purchase_timestamp, order_delivered_customer_date)) AS avg_delivery_days
FROM vw_sales_fact
WHERE order_purchase_timestamp BETWEEN ? AND ?
  AND order_delivered_customer_date IS NOT NULL
  AND review_score IS NOT NULL
  AND (? IS NULL OR product_category = ?)
GROUP BY 1
ORDER BY 1;

-- name: top_states
SELECT
  customer_state,
  SUM(payment_value) AS revenue
FROM vw_sales_fact
WHERE order_purchase_timestamp BETWEEN ? AND ?
  AND (? IS NULL OR product_category = ?)
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;

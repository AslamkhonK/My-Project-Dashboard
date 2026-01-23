-- 01_create_tables.sql

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS reviews;

CREATE TABLE customers (
  customer_id VARCHAR PRIMARY KEY,
  customer_unique_id VARCHAR,
  customer_zip_code_prefix VARCHAR,
  customer_city VARCHAR,
  customer_state VARCHAR
);

CREATE TABLE orders (
  order_id VARCHAR PRIMARY KEY,
  customer_id VARCHAR,
  order_status VARCHAR,
  order_purchase_timestamp TIMESTAMP,
  order_approved_at TIMESTAMP,
  order_delivered_carrier_date TIMESTAMP,
  order_delivered_customer_date TIMESTAMP,
  order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items (
  order_id VARCHAR,
  order_item_id INTEGER,
  product_id VARCHAR,
  seller_id VARCHAR,
  shipping_limit_date TIMESTAMP,
  price DOUBLE,
  freight_value DOUBLE
);

CREATE TABLE products (
  product_id VARCHAR PRIMARY KEY,
  product_category_name VARCHAR,
  product_name_lenght INTEGER,
  product_description_lenght INTEGER,
  product_photos_qty INTEGER,
  product_weight_g DOUBLE,
  product_length_cm DOUBLE,
  product_height_cm DOUBLE,
  product_width_cm DOUBLE
);

CREATE TABLE payments (
  order_id VARCHAR,
  payment_sequential INTEGER,
  payment_type VARCHAR,
  payment_installments INTEGER,
  payment_value DOUBLE
);

CREATE TABLE reviews (
  review_id VARCHAR,
  order_id VARCHAR,
  review_score INTEGER,
  review_comment_title VARCHAR,
  review_comment_message VARCHAR,
  review_creation_date TIMESTAMP,
  review_answer_timestamp TIMESTAMP
);

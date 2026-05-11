/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 04: Dynamic Tables Demo
  
  Demonstrates declarative data pipelines using Dynamic Tables
  as an alternative to traditional ETL orchestration.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PARTNERS_WH;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA ANALYTICS;

-- =========================================================================
-- PART 1: DYNAMIC TABLE - Customer 360 Summary
-- =========================================================================

CREATE OR REPLACE DYNAMIC TABLE customer_360
  TARGET_LAG = '1 hour'
  WAREHOUSE = PARTNERS_WH
AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    c.country,
    c.region,
    c.customer_tier,
    c.signup_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF('day', MAX(o.order_date), CURRENT_DATE()) AS days_since_last_order
FROM RAW.customers c
LEFT JOIN RAW.orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4, 5, 6, 7;

-- =========================================================================
-- PART 2: DYNAMIC TABLE - Sales Analytics
-- =========================================================================

CREATE OR REPLACE DYNAMIC TABLE sales_by_category
  TARGET_LAG = '1 hour'
  WAREHOUSE = PARTNERS_WH
AS
SELECT
    DATE_TRUNC('month', o.order_date) AS order_month,
    p.category,
    p.subcategory,
    COUNT(DISTINCT o.order_id) AS order_count,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.unit_price) AS gross_revenue,
    SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100) AS total_discounts,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS net_revenue,
    SUM(oi.quantity * (oi.unit_price - p.cost_price)) AS gross_margin
FROM RAW.orders o
JOIN RAW.order_items oi ON o.order_id = oi.order_id
JOIN RAW.products p ON oi.product_id = p.product_id
GROUP BY 1, 2, 3;

-- =========================================================================
-- PART 3: DYNAMIC TABLE - Top Products
-- =========================================================================

CREATE OR REPLACE DYNAMIC TABLE top_products
  TARGET_LAG = '1 hour'
  WAREHOUSE = PARTNERS_WH
AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    p.cost_price,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS total_revenue,
    SUM(oi.quantity * (oi.unit_price - p.cost_price)) AS total_margin,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.review_id) AS review_count
FROM RAW.products p
LEFT JOIN RAW.order_items oi ON p.product_id = oi.product_id
LEFT JOIN RAW.product_reviews r ON p.product_id = r.product_id
GROUP BY 1, 2, 3, 4, 5;

-- =========================================================================
-- QUERY: Verify dynamic tables
-- =========================================================================

SHOW DYNAMIC TABLES IN SCHEMA ANALYTICS;

SELECT * FROM customer_360 ORDER BY total_spent DESC LIMIT 10;

SELECT * FROM sales_by_category ORDER BY order_month, net_revenue DESC;

SELECT * FROM top_products ORDER BY total_revenue DESC;

SELECT 'Dynamic tables demo complete!' AS STATUS;

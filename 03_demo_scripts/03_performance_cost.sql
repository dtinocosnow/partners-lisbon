/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 03: Performance and Cost Demo
  
  Demonstrates warehouse sizing, caching behavior, auto-suspend/resume,
  and resource monitors.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA RAW;

-- =========================================================================
-- PART 1: WAREHOUSE SIZING COMPARISON
-- =========================================================================

-- Use XS warehouse
USE WAREHOUSE PARTNERS_WH;
ALTER WAREHOUSE PARTNERS_WH SET WAREHOUSE_SIZE = 'XSMALL';

SELECT
    p.category,
    p.subcategory,
    COUNT(DISTINCT o.order_id) AS order_count,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS net_revenue,
    AVG(oi.unit_price) AS avg_price,
    SUM(oi.quantity) AS total_units
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY 1, 2
ORDER BY net_revenue DESC;

-- Check query history for the execution time
SELECT
    query_id,
    query_text,
    warehouse_size,
    execution_status,
    total_elapsed_time / 1000 AS elapsed_seconds,
    bytes_scanned,
    rows_produced
FROM TABLE(information_schema.query_history(
    dateadd('minutes', -5, current_timestamp()),
    current_timestamp()
))
WHERE query_text LIKE '%category%subcategory%'
ORDER BY start_time DESC
LIMIT 1;

-- =========================================================================
-- PART 2: CACHING DEMO
-- =========================================================================

-- First execution - data from storage
SELECT
    c.country,
    c.customer_tier,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(o.total_amount) AS revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY 1, 2
ORDER BY revenue DESC;

-- Second execution - result cache (instant)
SELECT
    c.country,
    c.customer_tier,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(o.total_amount) AS revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY 1, 2
ORDER BY revenue DESC;

-- Compare execution times in query history
SELECT
    query_id,
    SUBSTR(query_text, 1, 60) AS query_preview,
    total_elapsed_time AS elapsed_ms,
    bytes_scanned,
    CASE WHEN bytes_scanned = 0 THEN 'RESULT CACHE HIT' ELSE 'FULL SCAN' END AS cache_status
FROM TABLE(information_schema.query_history(
    dateadd('minutes', -5, current_timestamp()),
    current_timestamp()
))
WHERE query_text LIKE '%customer_tier%order_status%'
ORDER BY start_time DESC
LIMIT 2;

-- =========================================================================
-- PART 3: WAREHOUSE MONITORING
-- =========================================================================

-- Show current warehouses
SHOW WAREHOUSES;

-- Auto-suspend demo: check warehouse state
SELECT
    'PARTNERS_WH' AS warehouse,
    CURRENT_WAREHOUSE() AS active_wh,
    'Auto-suspend: 60 seconds of inactivity' AS behavior;

-- Query to show credit usage concept (informational)
SELECT
    'XSMALL' AS wh_size, 1 AS credits_per_hour, '1 node' AS cluster_size
UNION ALL SELECT 'SMALL', 2, '1 node'
UNION ALL SELECT 'MEDIUM', 4, '1 node'
UNION ALL SELECT 'LARGE', 8, '1 node'
UNION ALL SELECT 'XLARGE', 16, '1 node'
UNION ALL SELECT '2XLARGE', 32, '1 node'
UNION ALL SELECT '3XLARGE', 64, '1 node'
UNION ALL SELECT '4XLARGE', 128, '1 node';

-- =========================================================================
-- PART 4: RESOURCE MONITOR (concept demo)
-- =========================================================================

CREATE OR REPLACE RESOURCE MONITOR partners_monitor
  WITH
    CREDIT_QUOTA = 100
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
      ON 75 PERCENT DO NOTIFY
      ON 90 PERCENT DO NOTIFY
      ON 100 PERCENT DO SUSPEND;

SELECT 'Performance and cost demo complete!' AS STATUS;

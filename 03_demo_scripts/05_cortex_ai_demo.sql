/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 05: Cortex AI Demo
  
  Demonstrates Cortex AI functions, Cortex Analyst with Semantic View,
  ML Functions (Forecast), and Cortex Search.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PARTNERS_WH;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA ANALYTICS;

-- =========================================================================
-- PART 1: CORTEX LLM FUNCTIONS
-- =========================================================================

-- Sentiment Analysis on product reviews
SELECT
    r.review_id,
    p.product_name,
    r.rating,
    SUBSTR(r.review_text, 1, 80) AS review_preview,
    SNOWFLAKE.CORTEX.SENTIMENT(r.review_text) AS sentiment_score
FROM RAW.product_reviews r
JOIN RAW.products p ON r.product_id = p.product_id
ORDER BY sentiment_score ASC;

-- Translation (English to Portuguese)
SELECT
    r.review_id,
    r.review_text AS original_en,
    SNOWFLAKE.CORTEX.TRANSLATE(r.review_text, 'en', 'pt') AS translated_pt
FROM RAW.product_reviews r
LIMIT 5;

-- Summarize reviews for a product
SELECT
    p.product_name,
    SNOWFLAKE.CORTEX.SUMMARIZE(
        LISTAGG(r.review_text, ' | ') WITHIN GROUP (ORDER BY r.review_date)
    ) AS review_summary
FROM RAW.product_reviews r
JOIN RAW.products p ON r.product_id = p.product_id
WHERE p.product_id = 101
GROUP BY p.product_name;

-- Classification
SELECT
    r.review_id,
    SUBSTR(r.review_text, 1, 60) AS review_preview,
    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(
        r.review_text,
        ['Product Quality', 'Customer Service', 'Value for Money', 'Technical Performance']
    ):label::STRING AS category
FROM RAW.product_reviews r;

-- AI Complete - Generate product description
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'snowflake-arctic',
    'Write a compelling 2-sentence product description for a high-performance 15-inch laptop aimed at data professionals. Focus on speed and reliability.'
) AS generated_description;

-- =========================================================================
-- PART 2: SEMANTIC VIEW FOR CORTEX ANALYST
-- =========================================================================

CREATE OR REPLACE SEMANTIC VIEW sv_sales_analytics

  TABLES (
    orders AS PARTNERS_LISBON_DEMO.RAW.ORDERS PRIMARY KEY (ORDER_ID),
    customers AS PARTNERS_LISBON_DEMO.RAW.CUSTOMERS PRIMARY KEY (CUSTOMER_ID),
    products AS PARTNERS_LISBON_DEMO.RAW.PRODUCTS PRIMARY KEY (PRODUCT_ID),
    order_items AS PARTNERS_LISBON_DEMO.RAW.ORDER_ITEMS PRIMARY KEY (ITEM_ID)
  )

  RELATIONSHIPS (
    orders_to_customers AS orders (CUSTOMER_ID) REFERENCES customers,
    items_to_orders AS order_items (ORDER_ID) REFERENCES orders,
    items_to_products AS order_items (PRODUCT_ID) REFERENCES products
  )

  FACTS (
    orders.order_revenue AS TOTAL_AMOUNT
      COMMENT = 'Revenue from a single order',
    order_items.line_revenue AS QUANTITY * UNIT_PRICE * (1 - DISCOUNT_PCT / 100)
      COMMENT = 'Net revenue for a line item after discount',
    products.product_cost AS COST_PRICE
      COMMENT = 'Product cost price'
  )

  DIMENSIONS (
    customers.customer_country AS COUNTRY
      WITH SYNONYMS = ('nation', 'location')
      COMMENT = 'Customer country',
    customers.customer_region AS REGION
      WITH SYNONYMS = ('area', 'geography')
      COMMENT = 'Geographic region: EMEA, AMER, APJ',
    customers.customer_tier AS CUSTOMER_TIER
      WITH SYNONYMS = ('tier', 'level', 'segment')
      COMMENT = 'Loyalty tier: Gold, Silver, Bronze',
    products.product_category AS CATEGORY
      WITH SYNONYMS = ('type', 'group')
      COMMENT = 'Product category',
    products.product_name_dim AS PRODUCT_NAME
      WITH SYNONYMS = ('product', 'item')
      COMMENT = 'Product display name',
    orders.order_date_dim AS ORDER_DATE
      WITH SYNONYMS = ('date', 'when', 'purchase date')
      COMMENT = 'Date when the order was placed',
    orders.order_month AS DATE_TRUNC('MONTH', ORDER_DATE)
      COMMENT = 'Month of the order',
    orders.order_status_dim AS ORDER_STATUS
      WITH SYNONYMS = ('status')
      COMMENT = 'Current status of the order'
  )

  METRICS (
    orders.total_revenue AS SUM(order_revenue)
      WITH SYNONYMS = ('revenue', 'sales', 'total sales')
      COMMENT = 'Total revenue across all orders',
    orders.total_orders AS COUNT(DISTINCT ORDER_ID)
      WITH SYNONYMS = ('order count', 'number of orders')
      COMMENT = 'Total number of orders',
    orders.average_order_value AS AVG(order_revenue)
      WITH SYNONYMS = ('AOV', 'avg order')
      COMMENT = 'Average value per order',
    orders.total_customers AS COUNT(DISTINCT CUSTOMER_ID)
      COMMENT = 'Total unique customers',
    order_items.net_line_revenue AS SUM(line_revenue)
      COMMENT = 'Total net revenue from line items after discounts',
    order_items.total_units_sold AS SUM(QUANTITY)
      COMMENT = 'Total units sold'
  )

  COMMENT = 'Sales analytics semantic view for Partner Enablement demo';

-- =========================================================================
-- PART 3: QUERY SEMANTIC VIEW (simulates Cortex Analyst output)
-- =========================================================================

-- Total revenue by country
SELECT
    c.country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM RAW.orders o
JOIN RAW.customers c ON o.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;

-- Monthly sales trend
SELECT
    DATE_TRUNC('month', o.order_date) AS order_month,
    COUNT(DISTINCT o.order_id) AS orders,
    SUM(o.total_amount) AS revenue
FROM RAW.orders o
GROUP BY 1
ORDER BY 1;

-- Top products by margin
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS net_revenue,
    SUM(oi.quantity * (oi.unit_price - p.cost_price)) AS gross_margin,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost_price)) /
          NULLIF(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 0) * 100, 1) AS margin_pct
FROM RAW.order_items oi
JOIN RAW.products p ON oi.product_id = p.product_id
GROUP BY 1, 2
ORDER BY gross_margin DESC;

-- =========================================================================
-- PART 4: ML FUNCTIONS - FORECAST
-- =========================================================================

-- Create daily sales view for forecasting
CREATE OR REPLACE VIEW daily_sales_for_forecast AS
SELECT
    order_date AS ds,
    SUM(total_amount) AS y
FROM RAW.orders
WHERE order_status IN ('Delivered', 'Shipped')
GROUP BY order_date
ORDER BY order_date;

SELECT * FROM daily_sales_for_forecast;

-- Create forecast model
CREATE OR REPLACE SNOWFLAKE.ML.FORECAST sales_forecast_model(
    INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'DAILY_SALES_FOR_FORECAST'),
    TIMESTAMP_COLNAME => 'DS',
    TARGET_COLNAME => 'Y'
);

-- Generate 30-day forecast
CALL sales_forecast_model!FORECAST(
    FORECASTING_PERIODS => 30
);

-- Store forecast results
CREATE OR REPLACE TABLE sales_forecast_results AS
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- View forecast
SELECT
    TS AS forecast_date,
    ROUND(FORECAST, 2) AS predicted_sales,
    ROUND(LOWER_BOUND, 2) AS lower_bound,
    ROUND(UPPER_BOUND, 2) AS upper_bound
FROM sales_forecast_results
ORDER BY TS;

-- =========================================================================
-- PART 5: CORTEX SEARCH (on product reviews)
-- =========================================================================

CREATE OR REPLACE TABLE RAW.reviews_for_search AS
SELECT
    r.review_id,
    p.product_name,
    p.category,
    r.rating,
    r.review_text,
    r.review_date
FROM RAW.product_reviews r
JOIN RAW.products p ON r.product_id = p.product_id;

CREATE OR REPLACE CORTEX SEARCH SERVICE reviews_search
  ON review_text
  ATTRIBUTES rating, category, product_name
  WAREHOUSE = PARTNERS_WH
  TARGET_LAG = '1 hour'
  AS (
    SELECT
      review_id,
      product_name,
      category,
      rating,
      review_text,
      review_date
    FROM RAW.reviews_for_search
  );

SELECT 'Cortex AI demo complete!' AS STATUS;

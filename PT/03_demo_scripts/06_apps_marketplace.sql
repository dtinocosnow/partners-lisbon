/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 06: Apps and Marketplace Concepts
  
  Demonstrates Streamlit in Snowflake concept, Native Apps framework,
  and marketplace / data sharing concepts.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PARTNERS_WH;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA ANALYTICS;

-- =========================================================================
-- PART 1: STREAMLIT IN SNOWFLAKE (Conceptual - show syntax)
-- =========================================================================

/*
NOTE: The following is the conceptual code for a Streamlit app.
In a real environment, you would create a Streamlit app via Snowsight UI
or using CREATE STREAMLIT command.

--- app.py (Streamlit code) ---

import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Partner Demo Dashboard", layout="wide")
st.title("Sales Analytics Dashboard")

col1, col2, col3 = st.columns(3)

revenue = session.sql("""
    SELECT SUM(total_amount) as total
    FROM PARTNERS_LISBON_DEMO.RAW.ORDERS
    WHERE order_status = 'Delivered'
""").collect()[0]['TOTAL']

orders = session.sql("""
    SELECT COUNT(*) as total
    FROM PARTNERS_LISBON_DEMO.RAW.ORDERS
""").collect()[0]['TOTAL']

customers = session.sql("""
    SELECT COUNT(DISTINCT customer_id) as total
    FROM PARTNERS_LISBON_DEMO.RAW.CUSTOMERS
""").collect()[0]['TOTAL']

col1.metric("Total Revenue", f"${revenue:,.2f}")
col2.metric("Total Orders", f"{orders}")
col3.metric("Total Customers", f"{customers}")

df_monthly = session.sql("""
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(total_amount) as revenue
    FROM PARTNERS_LISBON_DEMO.RAW.ORDERS
    WHERE order_status IN ('Delivered', 'Shipped')
    GROUP BY 1
    ORDER BY 1
""").to_pandas()

st.subheader("Monthly Revenue Trend")
st.line_chart(df_monthly.set_index('MONTH'))

df_products = session.sql("""
    SELECT
        p.product_name,
        SUM(oi.quantity * oi.unit_price) as revenue
    FROM PARTNERS_LISBON_DEMO.RAW.ORDER_ITEMS oi
    JOIN PARTNERS_LISBON_DEMO.RAW.PRODUCTS p ON oi.product_id = p.product_id
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10
""").to_pandas()

st.subheader("Top 10 Products by Revenue")
st.bar_chart(df_products.set_index('PRODUCT_NAME'))
*/

-- =========================================================================
-- PART 2: SECURE VIEW FOR SHARING
-- =========================================================================

CREATE OR REPLACE SECURE VIEW partner_analytics_view AS
SELECT
    DATE_TRUNC('month', o.order_date) AS order_month,
    c.country,
    c.region,
    p.category,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS net_revenue,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM RAW.orders o
JOIN RAW.customers c ON o.customer_id = c.customer_id
JOIN RAW.order_items oi ON o.order_id = oi.order_id
JOIN RAW.products p ON oi.product_id = p.product_id
GROUP BY 1, 2, 3, 4;

SELECT * FROM partner_analytics_view ORDER BY order_month, net_revenue DESC;

-- =========================================================================
-- PART 3: DATA SHARING CONCEPT
-- =========================================================================

/*
NOTE: Data sharing requires a second Snowflake account to demonstrate fully.
The following shows the syntax for creating a share.

-- Create a share
CREATE OR REPLACE SHARE partner_analytics_share
  COMMENT = 'Aggregated analytics data shared with partners';

-- Grant access to the secure view
GRANT USAGE ON DATABASE PARTNERS_LISBON_DEMO TO SHARE partner_analytics_share;
GRANT USAGE ON SCHEMA PARTNERS_LISBON_DEMO.ANALYTICS TO SHARE partner_analytics_share;
GRANT SELECT ON VIEW PARTNERS_LISBON_DEMO.ANALYTICS.partner_analytics_view
  TO SHARE partner_analytics_share;

-- Add consumer account
-- ALTER SHARE partner_analytics_share ADD ACCOUNTS = <consumer_account>;
*/

-- =========================================================================
-- PART 4: ZERO-COPY CLONE DEMO
-- =========================================================================

CREATE OR REPLACE DATABASE partners_lisbon_dev CLONE PARTNERS_LISBON_DEMO;

SELECT 'Clone created!' AS STATUS;

SELECT
    table_catalog,
    table_schema,
    table_name,
    row_count
FROM partners_lisbon_dev.information_schema.tables
WHERE table_schema = 'RAW'
ORDER BY table_name;

DROP DATABASE partners_lisbon_dev;

-- =========================================================================
-- PART 5: TAGS AND CLASSIFICATION (Horizon Catalog preview)
-- =========================================================================

CREATE OR REPLACE TAG GOVERNANCE.data_classification
  ALLOWED_VALUES 'PII', 'SENSITIVE', 'PUBLIC', 'INTERNAL'
  COMMENT = 'Data classification tag for governance';

ALTER TABLE RAW.customers MODIFY COLUMN email
  SET TAG GOVERNANCE.data_classification = 'PII';
ALTER TABLE RAW.customers MODIFY COLUMN phone
  SET TAG GOVERNANCE.data_classification = 'PII';
ALTER TABLE RAW.customers MODIFY COLUMN first_name
  SET TAG GOVERNANCE.data_classification = 'PII';
ALTER TABLE RAW.customers MODIFY COLUMN last_name
  SET TAG GOVERNANCE.data_classification = 'PII';
ALTER TABLE RAW.customers MODIFY COLUMN city
  SET TAG GOVERNANCE.data_classification = 'INTERNAL';

-- Show tagged columns
SELECT
    tag_name,
    tag_value,
    object_name,
    column_name
FROM TABLE(
    PARTNERS_LISBON_DEMO.information_schema.tag_references(
        'PARTNERS_LISBON_DEMO.RAW.CUSTOMERS',
        'TABLE'
    )
)
ORDER BY column_name;

SELECT 'Apps and marketplace demo complete!' AS STATUS;

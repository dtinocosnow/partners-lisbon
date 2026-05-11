/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 02: Governance Demo
  
  Demonstrates RBAC, masking policies, and row access policies.
  Shows same query returning different results based on role.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PARTNERS_WH;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA GOVERNANCE;

-- =========================================================================
-- PART 1: MASKING POLICIES
-- =========================================================================

CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'ENGINEER_ROLE') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '****@')
  END;

CREATE OR REPLACE MASKING POLICY mask_phone AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'ENGINEER_ROLE') THEN val
    ELSE REGEXP_REPLACE(val, '[0-9]', '*')
  END;

ALTER TABLE RAW.customers
  MODIFY COLUMN email SET MASKING POLICY mask_email;

ALTER TABLE RAW.customers
  MODIFY COLUMN phone SET MASKING POLICY mask_phone;

-- =========================================================================
-- DEMO: Show the effect of masking
-- =========================================================================

-- As ACCOUNTADMIN: full data visible
SELECT customer_id, first_name, last_name, email, phone, city, country
FROM RAW.customers
LIMIT 5;

-- As ANALYST_ROLE: masked data
USE ROLE ANALYST_ROLE;
USE WAREHOUSE PARTNERS_WH;

SELECT customer_id, first_name, last_name, email, phone, city, country
FROM PARTNERS_LISBON_DEMO.RAW.customers
LIMIT 5;

-- Back to ACCOUNTADMIN
USE ROLE ACCOUNTADMIN;

-- =========================================================================
-- PART 2: ROW ACCESS POLICY
-- =========================================================================

USE SCHEMA GOVERNANCE;

CREATE OR REPLACE ROW ACCESS POLICY region_access_policy
  AS (region_val VARCHAR) RETURNS BOOLEAN ->
  CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'ENGINEER_ROLE') THEN TRUE
    WHEN CURRENT_ROLE() = 'ANALYST_ROLE' AND region_val = 'EMEA' THEN TRUE
    ELSE FALSE
  END;

ALTER TABLE RAW.customers
  ADD ROW ACCESS POLICY region_access_policy ON (region);

-- =========================================================================
-- DEMO: Show the effect of row access
-- =========================================================================

-- As ACCOUNTADMIN: all regions visible
SELECT region, COUNT(*) AS customer_count
FROM RAW.customers
GROUP BY region
ORDER BY region;

-- As ANALYST_ROLE: only EMEA visible
USE ROLE ANALYST_ROLE;
USE WAREHOUSE PARTNERS_WH;

SELECT region, COUNT(*) AS customer_count
FROM PARTNERS_LISBON_DEMO.RAW.customers
GROUP BY region
ORDER BY region;

-- Back to ACCOUNTADMIN
USE ROLE ACCOUNTADMIN;

-- =========================================================================
-- PART 3: Combined effect
-- =========================================================================

-- Full view (ACCOUNTADMIN)
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    c.city,
    c.country,
    c.region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM RAW.customers c
LEFT JOIN RAW.orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY total_spent DESC;

-- Restricted view (ANALYST_ROLE): masked PII + EMEA only
USE ROLE ANALYST_ROLE;
USE WAREHOUSE PARTNERS_WH;

SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.phone,
    c.city,
    c.country,
    c.region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM PARTNERS_LISBON_DEMO.RAW.customers c
LEFT JOIN PARTNERS_LISBON_DEMO.RAW.orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY total_spent DESC;

USE ROLE ACCOUNTADMIN;

SELECT 'Governance demo complete!' AS STATUS;

/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 99: Cleanup
  
  Removes all objects created during the demo.
  Run this after the session to clean up.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS PARTNERS_LISBON_DEMO;
DROP DATABASE IF EXISTS partners_lisbon_dev;
DROP WAREHOUSE IF EXISTS PARTNERS_WH;
DROP WAREHOUSE IF EXISTS PARTNERS_WH_MEDIUM;
DROP ROLE IF EXISTS ANALYST_ROLE;
DROP ROLE IF EXISTS ENGINEER_ROLE;
DROP RESOURCE MONITOR IF EXISTS partners_monitor;

SELECT 'Cleanup complete! All demo objects removed.' AS STATUS;

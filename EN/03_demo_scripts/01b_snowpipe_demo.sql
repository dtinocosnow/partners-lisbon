-- =============================================================================
-- SNOWPIPE DEMO - Partner Enablement Lisbon
-- Demonstration of continuous data ingestion
-- =============================================================================

USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA RAW;
USE WAREHOUSE PARTNERS_WH;

-- =============================================================================
-- PART 1: Create an internal stage to simulate incoming files
-- =============================================================================

CREATE OR REPLACE STAGE partners_ingest_stage
  FILE_FORMAT = (TYPE = 'JSON');

-- =============================================================================
-- PART 2: Create the target table for streaming events
-- =============================================================================

CREATE OR REPLACE TABLE raw_events (
    event_id STRING,
    event_type STRING,
    user_id STRING,
    event_timestamp TIMESTAMP_NTZ,
    payload VARIANT,
    loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- PART 3: Create the Pipe (automatic ingestion)
-- =============================================================================

-- Snowpipe: defines the COPY INTO that will be executed automatically
-- when new files arrive at the stage
CREATE OR REPLACE PIPE partners_event_pipe
  AUTO_INGEST = FALSE  -- For demo we use FALSE (manual trigger)
  -- In production: AUTO_INGEST = TRUE with S3/Azure/GCS notification
  AS
  COPY INTO raw_events (event_id, event_type, user_id, event_timestamp, payload)
  FROM (
    SELECT 
      $1:event_id::STRING,
      $1:event_type::STRING,
      $1:user_id::STRING,
      $1:event_timestamp::TIMESTAMP_NTZ,
      $1
    FROM @partners_ingest_stage
  )
  FILE_FORMAT = (TYPE = 'JSON');

-- =============================================================================
-- PART 4: Simulate file loading and ingestion
-- =============================================================================

-- Create a sample JSON file in the stage
COPY INTO @partners_ingest_stage/events_batch_001.json
FROM (
    SELECT OBJECT_CONSTRUCT(
        'event_id', UUID_STRING(),
        'event_type', 'page_view',
        'user_id', 'user_' || SEQ4()::STRING,
        'event_timestamp', DATEADD('minute', -SEQ4(), CURRENT_TIMESTAMP())
    ) AS json_data
    FROM TABLE(GENERATOR(ROWCOUNT => 20))
)
FILE_FORMAT = (TYPE = 'JSON');

-- Verify that the file is in the stage
LIST @partners_ingest_stage;

-- =============================================================================
-- PART 5: Execute the pipe manually (simulates AUTO_INGEST)
-- =============================================================================

-- In production, this happens AUTOMATICALLY when files arrive at S3/Azure/GCS
ALTER PIPE partners_event_pipe REFRESH;

-- Wait 5-10 seconds for the pipe to process...
-- (In demo, we can use SYSTEM$PIPE_STATUS to verify)
SELECT SYSTEM$PIPE_STATUS('partners_event_pipe') AS pipe_status;

-- Verify loaded data
SELECT COUNT(*) AS events_loaded FROM raw_events;
SELECT * FROM raw_events LIMIT 5;

-- =============================================================================
-- PART 6: Show the Snowpipe Streaming concept (sub-second latency)
-- =============================================================================

-- Snowpipe Streaming: for SECONDS latency (vs minutes with classic Snowpipe)
-- Uses the Snowflake Ingest SDK (Java/Python) to send rows directly
-- No intermediate files!

-- Concept (not executable here, but show the diagram):
/*
  [Application/IoT/Kafka] 
       |
       v
  [Snowflake Ingest SDK - SnowflakeStreamingIngestClient]
       |
       v (rows inserted directly, latency < 1 second)
  [Snowflake Table]

  Comparison:
  +---------------------+----------------+-------------------+
  | Method              | Latency        | Use Case          |
  +---------------------+----------------+-------------------+
  | COPY INTO           | Minutes        | Scheduled batch   |
  | Snowpipe            | ~1 minute      | Continuous (files)|
  | Snowpipe Streaming  | < 10 seconds   | Real-time events  |
  +---------------------+----------------+-------------------+
*/

-- =============================================================================
-- PART 7: Pipe verification and history
-- =============================================================================

-- Pipe load history
SELECT *
FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'RAW_EVENTS',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));

-- Detailed pipe status
DESCRIBE PIPE partners_event_pipe;

-- =============================================================================
-- MESSAGE FOR THE CUSTOMER:
-- "Snowpipe eliminates the need to orchestrate loads. Data arrives at the stage,
--  the pipe detects it automatically and loads it. Zero cron jobs, zero Airflow for ingestion."
-- =============================================================================

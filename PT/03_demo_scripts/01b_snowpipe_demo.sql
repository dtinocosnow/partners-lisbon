-- =============================================================================
-- SNOWPIPE DEMO - Partner Enablement Lisboa
-- Demonstracao de ingestao continua de dados
-- =============================================================================

USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA RAW;
USE WAREHOUSE PARTNERS_WH;

-- =============================================================================
-- PARTE 1: Criar um stage interno para simular ficheiros a chegar
-- =============================================================================

CREATE OR REPLACE STAGE partners_ingest_stage
  FILE_FORMAT = (TYPE = 'JSON');

-- =============================================================================
-- PARTE 2: Criar a tabela de destino para eventos de streaming
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
-- PARTE 3: Criar o Pipe (ingestao automatica)
-- =============================================================================

-- Snowpipe: define o COPY INTO que sera executado automaticamente
-- quando novos ficheiros chegam ao stage
CREATE OR REPLACE PIPE partners_event_pipe
  AUTO_INGEST = FALSE  -- Para demo usamos FALSE (manual trigger)
  -- Em producao: AUTO_INGEST = TRUE com notificacao S3/Azure/GCS
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
-- PARTE 4: Simular carga de ficheiros e ingestao
-- =============================================================================

-- Criar um ficheiro JSON de exemplo no stage
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

-- Verificar que o ficheiro esta no stage
LIST @partners_ingest_stage;

-- =============================================================================
-- PARTE 5: Executar o pipe manualmente (simula AUTO_INGEST)
-- =============================================================================

-- Em producao, isto acontece AUTOMATICAMENTE quando ficheiros chegam ao S3/Azure/GCS
ALTER PIPE partners_event_pipe REFRESH;

-- Aguardar 5-10 segundos para o pipe processar...
-- (Em demo, podemos usar SYSTEM$PIPE_STATUS para verificar)
SELECT SYSTEM$PIPE_STATUS('partners_event_pipe') AS pipe_status;

-- Verificar dados carregados
SELECT COUNT(*) AS events_loaded FROM raw_events;
SELECT * FROM raw_events LIMIT 5;

-- =============================================================================
-- PARTE 6: Mostrar o conceito de Snowpipe Streaming (latencia sub-segundo)
-- =============================================================================

-- Snowpipe Streaming: para latencia de SEGUNDOS (vs minutos do Snowpipe classico)
-- Usa a Snowflake Ingest SDK (Java/Python) para enviar rows directamente
-- Sem ficheiros intermedios!

-- Conceito (nao executavel aqui, mas mostrar o diagrama):
/*
  [Aplicacao/IoT/Kafka] 
       |
       v
  [Snowflake Ingest SDK - SnowflakeStreamingIngestClient]
       |
       v (rows inseridas directamente, latencia < 1 segundo)
  [Tabela Snowflake]

  Comparacao:
  +---------------------+----------------+-------------------+
  | Metodo              | Latencia       | Caso de Uso       |
  +---------------------+----------------+-------------------+
  | COPY INTO           | Minutos        | Batch agendado    |
  | Snowpipe            | ~1 minuto      | Continuo (files)  |
  | Snowpipe Streaming  | < 10 segundos  | Real-time events  |
  +---------------------+----------------+-------------------+
*/

-- =============================================================================
-- PARTE 7: Verificacao do pipe e historico
-- =============================================================================

-- Historico de cargas do pipe
SELECT *
FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'RAW_EVENTS',
    START_TIME => DATEADD('hour', -1, CURRENT_TIMESTAMP())
));

-- Status detalhado do pipe
DESCRIBE PIPE partners_event_pipe;

-- =============================================================================
-- MENSAGEM PARA O CLIENTE:
-- "Snowpipe elimina a necessidade de orquestrar cargas. Os dados chegam ao stage,
--  o pipe detecta automaticamente e carrega. Zero cron jobs, zero Airflow para ingestao."
-- =============================================================================

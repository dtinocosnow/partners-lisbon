# Laboratorio Pratico Guiado - Snowflake Partner Enablement

> **Duracao:** ~30 minutos
> **Formato:** Exercicio acompanhado (follow-along)
> **Requisitos:** Conta Snowflake trial ou conta de demonstracao

---

## Objetivo

Neste laboratorio, vao construir um mini-pipeline de dados completo:
de zero a insights com governanca e IA.

**O que vamos fazer:**
1. Criar uma base de dados e schema
2. Carregar dados de amostra
3. Escrever queries analiticas
4. Aplicar uma politica de governanca
5. Utilizar uma funcao de IA Cortex

---

## Pre-requisitos

- [ ] Browser aberto em **https://app.snowflake.com**
- [ ] Sessao iniciada na vossa conta
- [ ] Role **ACCOUNTADMIN** selecionado (canto inferior esquerdo)
- [ ] Abrir uma **SQL Worksheet** (botao `+` > SQL Worksheet)

---

## Passo 1: Criar a Base de Dados e Schema

> **Objetivo:** Criar a estrutura base para o nosso projeto.

Copiem e executem o seguinte codigo na vossa SQL Worksheet:

```sql
-- Step 1: Create database and schema
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE DATABASE MY_PARTNER_LAB;
CREATE SCHEMA MY_PARTNER_LAB.RAW;
CREATE SCHEMA MY_PARTNER_LAB.ANALYTICS;

-- Create a warehouse (compute)
CREATE OR REPLACE WAREHOUSE MY_LAB_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE WAREHOUSE MY_LAB_WH;
USE DATABASE MY_PARTNER_LAB;
USE SCHEMA RAW;
```

**Resultado esperado:** Deverao ver mensagens de sucesso para cada comando.

> **Nota:** Reparem como o warehouse e criado em segundos. No Snowflake,
> computacao e elastica - podemos criar e destruir warehouses instantaneamente.

---

## Passo 2: Criar e Carregar Dados

> **Objetivo:** Criar tabelas e inserir dados de amostra de uma loja online.

```sql
-- Step 2: Create tables and load sample data
CREATE OR REPLACE TABLE customers (
    customer_id   INTEGER,
    name          VARCHAR(100),
    email         VARCHAR(100),
    country       VARCHAR(50),
    region        VARCHAR(20),
    tier          VARCHAR(20)
);

INSERT INTO customers VALUES
(1, 'Maria Santos', 'maria@email.pt', 'Portugal', 'EMEA', 'Gold'),
(2, 'Pedro Costa', 'pedro@email.pt', 'Portugal', 'EMEA', 'Silver'),
(3, 'Ana Ferreira', 'ana@email.pt', 'Portugal', 'EMEA', 'Bronze'),
(4, 'John Smith', 'john@email.com', 'United States', 'AMER', 'Gold'),
(5, 'Hans Mueller', 'hans@email.de', 'Germany', 'EMEA', 'Silver'),
(6, 'Yuki Tanaka', 'yuki@email.jp', 'Japan', 'APJ', 'Gold');

CREATE OR REPLACE TABLE orders (
    order_id      INTEGER,
    customer_id   INTEGER,
    order_date    DATE,
    amount        DECIMAL(10,2),
    status        VARCHAR(20)
);

INSERT INTO orders VALUES
(1001, 1, '2025-01-15', 1299.99, 'Delivered'),
(1002, 2, '2025-02-10', 499.99, 'Delivered'),
(1003, 1, '2025-02-20', 799.99, 'Delivered'),
(1004, 3, '2025-03-05', 149.99, 'Delivered'),
(1005, 4, '2025-03-15', 2199.99, 'Delivered'),
(1006, 5, '2025-04-01', 349.99, 'Shipped'),
(1007, 6, '2025-04-10', 899.99, 'Shipped'),
(1008, 1, '2025-05-01', 599.99, 'Processing'),
(1009, 4, '2025-05-15', 1499.99, 'Pending'),
(1010, 2, '2025-06-01', 249.99, 'Pending');

-- Verify data loaded
SELECT 'Customers: ' || COUNT(*) FROM customers;
SELECT 'Orders: ' || COUNT(*) FROM orders;
```

**Resultado esperado:** 6 clientes e 10 encomendas carregados.

---

## Passo 3: Queries Analiticas

> **Objetivo:** Escrever queries para extrair insights dos dados.

### 3a. Receita total por cliente

```sql
-- Step 3a: Revenue by customer
SELECT
    c.name,
    c.country,
    c.tier,
    COUNT(o.order_id) AS total_orders,
    SUM(o.amount) AS total_revenue,
    AVG(o.amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 1, 2, 3
ORDER BY total_revenue DESC;
```

**Pergunta:** Quem e o cliente com maior receita? De que pais?

### 3b. Receita mensal

```sql
-- Step 3b: Monthly revenue trend
SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS orders,
    SUM(amount) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

### 3c. Distribuicao por regiao

```sql
-- Step 3c: Revenue by region
SELECT
    c.region,
    COUNT(DISTINCT c.customer_id) AS customers,
    SUM(o.amount) AS total_revenue,
    ROUND(SUM(o.amount) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 1
ORDER BY total_revenue DESC;
```

---

## Passo 4: Aplicar Governanca

> **Objetivo:** Proteger dados sensiveis com uma masking policy.

### 4a. Criar uma masking policy para o email

```sql
-- Step 4a: Create masking policy
USE SCHEMA ANALYTICS;

CREATE OR REPLACE MASKING POLICY mask_email AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN') THEN val
    ELSE '****@****'
  END;

-- Apply to the email column
ALTER TABLE RAW.customers
  MODIFY COLUMN email SET MASKING POLICY mask_email;
```

### 4b. Criar um role e testar

```sql
-- Step 4b: Create a role and test
CREATE ROLE IF NOT EXISTS LAB_ANALYST;
GRANT USAGE ON DATABASE MY_PARTNER_LAB TO ROLE LAB_ANALYST;
GRANT USAGE ON ALL SCHEMAS IN DATABASE MY_PARTNER_LAB TO ROLE LAB_ANALYST;
GRANT SELECT ON ALL TABLES IN SCHEMA MY_PARTNER_LAB.RAW TO ROLE LAB_ANALYST;
GRANT USAGE ON WAREHOUSE MY_LAB_WH TO ROLE LAB_ANALYST;
GRANT ROLE LAB_ANALYST TO ROLE SYSADMIN;

-- Query as ACCOUNTADMIN (full access)
SELECT name, email, country FROM RAW.customers LIMIT 3;

-- Switch to LAB_ANALYST role
USE ROLE LAB_ANALYST;
USE WAREHOUSE MY_LAB_WH;

-- Same query - emails are now masked!
SELECT name, email, country FROM MY_PARTNER_LAB.RAW.customers LIMIT 3;

-- Switch back
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE MY_LAB_WH;
```

**Resultado esperado:** Com ACCOUNTADMIN os emails sao visiveis.
Com LAB_ANALYST aparecem como `****@****`.

> **Mensagem-chave:** A mesma tabela, a mesma query, resultados diferentes
> com base no role do utilizador. Isto e governanca nativa.

---

## Passo 5: Utilizar Cortex AI

> **Objetivo:** Chamar funcoes de IA diretamente em SQL.

### 5a. Analise de sentimento

```sql
-- Step 5a: Sentiment analysis
USE DATABASE MY_PARTNER_LAB;
USE SCHEMA RAW;

SELECT
    'The product quality is excellent, very happy with my purchase!' AS review,
    SNOWFLAKE.CORTEX.SENTIMENT(
        'The product quality is excellent, very happy with my purchase!'
    ) AS sentiment_score
UNION ALL
SELECT
    'Terrible experience. The product broke after one week.',
    SNOWFLAKE.CORTEX.SENTIMENT(
        'Terrible experience. The product broke after one week.'
    )
UNION ALL
SELECT
    'It is an okay product. Nothing special but works fine.',
    SNOWFLAKE.CORTEX.SENTIMENT(
        'It is an okay product. Nothing special but works fine.'
    );
```

**Resultado esperado:** Scores positivos (~0.9), negativos (~-0.8) e neutros (~0).

### 5b. Traducao automatica

```sql
-- Step 5b: Translation
SELECT
    'Snowflake is the AI Data Cloud platform' AS original,
    SNOWFLAKE.CORTEX.TRANSLATE(
        'Snowflake is the AI Data Cloud platform',
        'en',
        'pt'
    ) AS portuguese;
```

### 5c. Gerar texto com IA

```sql
-- Step 5c: AI text generation
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'snowflake-arctic',
    'In one paragraph, explain why data governance is important for organizations. Be concise.'
) AS ai_response;
```

> **Mensagem-chave:** Funcoes de IA chamadas diretamente em SQL.
> Sem necessidade de APIs externas, sem mover dados, sem infraestrutura adicional.

---

## Limpeza (Opcional)

Se quiserem limpar o ambiente apos o laboratorio:

```sql
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS MY_PARTNER_LAB;
DROP WAREHOUSE IF EXISTS MY_LAB_WH;
DROP ROLE IF EXISTS LAB_ANALYST;
```

---

## Parabens!

Completaram o laboratorio com sucesso. Nesta sessao pratica:

- **Criaram** uma base de dados e warehouse do zero
- **Carregaram** e consultaram dados
- **Aplicaram** governanca com masking policies
- **Utilizaram** IA com Cortex AI (sentimento, traducao, geracao de texto)

### Proximos passos recomendados:

1. **Zero to Snowflake Quickstart:** https://quickstarts.snowflake.com/guide/getting_started_with_snowflake
2. **Cortex AI Tutorial:** https://quickstarts.snowflake.com/guide/getting_started_with_cortex
3. **Snowflake University:** https://learn.snowflake.com

---

*Snowflake AI Data Cloud - A plataforma que unifica dados, IA e aplicacoes*

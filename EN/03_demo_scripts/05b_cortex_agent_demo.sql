-- =============================================================================
-- CORTEX AGENT DEMO - Partner Enablement Lisbon
-- Demonstration of Cortex Agents: intelligent orchestration with Analyst + Search
-- =============================================================================

USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA ANALYTICS;
USE WAREHOUSE PARTNERS_WH;

-- =============================================================================
-- PART 1: Context - What resources do we already have?
-- =============================================================================

-- We already have created:
-- 1. Semantic View: sv_sales_analytics (structured data - sales, customers, products)
-- 2. Cortex Search Service: reviews_search (unstructured data - product reviews)

-- Verify they exist
DESCRIBE SEMANTIC VIEW sv_sales_analytics;
SHOW CORTEX SEARCH SERVICES IN SCHEMA ANALYTICS;

-- =============================================================================
-- PART 2: Create the Cortex Agent
-- Combines Analyst (structured data) + Search (documents) into a single entry point
-- =============================================================================

CREATE OR REPLACE AGENT partners_sales_agent
  COMMENT = 'Agent for sales analysis and reviews - Partner Enablement Demo'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  orchestration:
    budget:
      seconds: 30
      tokens: 16000

  instructions:
    system: "You are a helpful sales analytics assistant for an e-commerce company. You help users understand sales performance and customer feedback."
    orchestration: "Use the sales_analyst tool for questions about revenue, orders, customers, and products. Use the reviews_search tool for questions about customer feedback, reviews, and product quality."
    response: "Respond concisely in Portuguese (Portugal). Include relevant numbers and data points. If showing revenue, use EUR currency format."
    sample_questions:
      - question: "Quais sao as vendas totais por regiao?"
        answer: "Vou analisar os dados de vendas por regiao usando a nossa base de dados."
      - question: "O que dizem os clientes sobre a qualidade dos produtos?"
        answer: "Vou pesquisar nas reviews dos clientes sobre qualidade de produtos."
      - question: "Qual o produto com melhor feedback?"
        answer: "Vou combinar dados de vendas com reviews para identificar o produto melhor avaliado."

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "sales_analyst"
        description: "Analyses structured sales data including orders, customers, products, and revenue metrics. Use for questions about sales figures, top customers, product performance, and business KPIs."
    - tool_spec:
        type: "cortex_search"
        name: "reviews_search"
        description: "Searches customer product reviews for feedback, complaints, and sentiment. Use for questions about customer opinions, product quality, and satisfaction."
    - tool_spec:
        type: "data_to_chart"
        name: "data_to_chart"
        description: "Generates visualizations from data results."

  tool_resources:
    sales_analyst:
      semantic_view: "PARTNERS_LISBON_DEMO.ANALYTICS.SV_SALES_ANALYTICS"
    reviews_search:
      name: "PARTNERS_LISBON_DEMO.ANALYTICS.REVIEWS_SEARCH"
      max_results: "5"
      title_column: "PRODUCT_NAME"
  $$;

-- =============================================================================
-- PART 3: Verify that the Agent was created
-- =============================================================================

SHOW AGENTS IN SCHEMA ANALYTICS;
DESCRIBE AGENT partners_sales_agent;

-- =============================================================================
-- PART 4: Test the Agent (NOTE: test via Snowsight UI > AI & ML > Agents)
-- =============================================================================

-- The Agent is used interactively via:
-- 1. Snowsight UI: AI & ML > Agents > partners_sales_agent
-- 2. REST API (for application integration)
-- 3. Snowflake Intelligence (for end users)

-- Suggested test questions:
-- "Quais sao as vendas totais por regiao?"
-- "Qual o cliente que mais gastou?"
-- "O que dizem as reviews sobre qualidade?"
-- "Compara as vendas da regiao EMEA com o feedback dos clientes dessa regiao"

-- =============================================================================
-- PART 5: Grant access to the Agent
-- =============================================================================

-- Grant access to ANALYST_ROLE so that other users can use the Agent
GRANT USAGE ON AGENT ANALYTICS.partners_sales_agent TO ROLE ANALYST_ROLE;

-- =============================================================================
-- MESSAGE FOR THE CUSTOMER:
-- "An Agent combines ALL your data - structured and unstructured - 
--  into a single intelligent assistant. The user asks questions in natural 
--  language, the Agent decides which tool to use (SQL for data, Search for 
--  documents) and returns an integrated response."
--
-- "To test it live, let's go to Snowsight > AI & ML > Agents"
-- =============================================================================

-- =============================================================================
-- PART 6: Click-Through Guide (show in the product)
-- =============================================================================

/*
DEMO CLICK-THROUGH in Snowsight:

1. Navigate to: AI & ML > Agents
2. Select: partners_sales_agent
3. In the playground, ask:
   - "Quais sao as vendas totais por regiao?"
   - Show how the Agent generates SQL via Cortex Analyst
   - Show the result with real data

4. Then ask:
   - "O que dizem os clientes sobre os nossos produtos?"
   - Show how the Agent uses Cortex Search
   - Show the review results

5. Complex question (uses BOTH tools):
   - "Qual o produto mais vendido e o que dizem as reviews sobre ele?"
   - Show how the Agent orchestrates: first fetches top product (Analyst)
     then fetches reviews for that product (Search)

ESTIMATED TIME: 5-8 minutes of demo
*/

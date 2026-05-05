-- =============================================================================
-- CORTEX AGENT DEMO - Partner Enablement Lisboa
-- Demonstracao de Cortex Agents: orquestracao inteligente com Analyst + Search
-- =============================================================================

USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA ANALYTICS;
USE WAREHOUSE PARTNERS_WH;

-- =============================================================================
-- PARTE 1: Contexto - Que recursos ja temos?
-- =============================================================================

-- Ja temos criados:
-- 1. Semantic View: sv_sales_analytics (dados estruturados - vendas, clientes, produtos)
-- 2. Cortex Search Service: reviews_search (dados nao-estruturados - reviews de produtos)

-- Verificar que existem
DESCRIBE SEMANTIC VIEW sv_sales_analytics;
SHOW CORTEX SEARCH SERVICES IN SCHEMA ANALYTICS;

-- =============================================================================
-- PARTE 2: Criar o Cortex Agent
-- Combina Analyst (dados estruturados) + Search (documentos) num unico ponto de entrada
-- =============================================================================

CREATE OR REPLACE AGENT partners_sales_agent
  COMMENT = 'Agent para analise de vendas e reviews - Partner Enablement Demo'
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
-- PARTE 3: Verificar que o Agent foi criado
-- =============================================================================

SHOW AGENTS IN SCHEMA ANALYTICS;
DESCRIBE AGENT partners_sales_agent;

-- =============================================================================
-- PARTE 4: Testar o Agent (NOTA: testar via Snowsight UI > AI & ML > Agents)
-- =============================================================================

-- O Agent e utilizado interactivamente via:
-- 1. Snowsight UI: AI & ML > Agents > partners_sales_agent
-- 2. REST API (para integracao em aplicacoes)
-- 3. Snowflake Intelligence (para utilizadores finais)

-- Perguntas de teste sugeridas:
-- "Quais sao as vendas totais por regiao?"
-- "Qual o cliente que mais gastou?"
-- "O que dizem as reviews sobre qualidade?"
-- "Compara as vendas da regiao EMEA com o feedback dos clientes dessa regiao"

-- =============================================================================
-- PARTE 5: Dar acesso ao Agent
-- =============================================================================

-- Dar acesso ao ANALYST_ROLE para que outros utilizadores possam usar o Agent
GRANT USAGE ON AGENT ANALYTICS.partners_sales_agent TO ROLE ANALYST_ROLE;

-- =============================================================================
-- MENSAGEM PARA O CLIENTE:
-- "Um Agent combina TODOS os vossos dados - estruturados e nao-estruturados - 
--  num unico assistente inteligente. O utilizador faz perguntas em linguagem 
--  natural, o Agent decide qual ferramenta usar (SQL para dados, Search para 
--  documentos) e devolve uma resposta integrada."
--
-- "Para testar ao vivo, vamos ao Snowsight > AI & ML > Agents"
-- =============================================================================

-- =============================================================================
-- PARTE 6: Click-Through Guide (mostrar no produto)
-- =============================================================================

/*
DEMO CLICK-THROUGH no Snowsight:

1. Navegar a: AI & ML > Agents
2. Selecionar: partners_sales_agent
3. No playground, perguntar:
   - "Quais sao as vendas totais por regiao?"
   - Mostrar como o Agent gera SQL via Cortex Analyst
   - Mostrar o resultado com dados reais

4. Depois perguntar:
   - "O que dizem os clientes sobre os nossos produtos?"
   - Mostrar como o Agent usa Cortex Search
   - Mostrar os resultados das reviews

5. Pergunta complexa (usa AMBAS as ferramentas):
   - "Qual o produto mais vendido e o que dizem as reviews sobre ele?"
   - Mostrar como o Agent orquestra: primeiro busca top produto (Analyst)
     depois busca reviews desse produto (Search)

TEMPO ESTIMADO: 5-8 minutos de demo
*/

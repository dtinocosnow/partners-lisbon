/*
=============================================================================
  SUPERNOVA SUPERMERCADOS - LABORATORIO PRATICO
  Script: Passo 4 - Criar Cortex Agent (Analista de Vendas)
  
  Pre-requisitos: Ter executado os passos 1-3 (Bronze, dbt Gold, Streamlit)
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE DATABASE SUPERNOVA_LAB;
USE WAREHOUSE SUPERNOVA_WH;
USE SCHEMA GOLD;

-- =============================================================================
-- PARTE 1: Criar Semantic View para dados estruturados
-- =============================================================================

CREATE OR REPLACE SEMANTIC VIEW SV_SUPERNOVA
  TABLES (
    kpi AS SUPERNOVA_LAB.GOLD.KPI_DIARIO PRIMARY KEY (DATA_VENDA, LOJA_ID),
    cat AS SUPERNOVA_LAB.GOLD.VENDAS_CATEGORIA_MENSAL PRIMARY KEY (MES, CATEGORIA),
    top AS SUPERNOVA_LAB.GOLD.TOP_PRODUTOS PRIMARY KEY (PRODUTO_ID),
    infl AS SUPERNOVA_LAB.GOLD.INFLACAO_VS_VENDAS PRIMARY KEY (MES)
  )
  DIMENSIONS (
    kpi.data_venda AS DATA_VENDA COMMENT = 'Data da venda',
    kpi.loja_id AS LOJA_ID COMMENT = 'ID da loja',
    kpi.nome_loja AS NOME_LOJA COMMENT = 'Nome da loja SuperNova',
    cat.categoria AS CATEGORIA COMMENT = 'Categoria de produto',
    cat.mes AS MES_CATEGORIA COMMENT = 'Mes de referencia para vendas por categoria',
    top.nome_produto AS NOME_PRODUTO COMMENT = 'Nome do produto',
    top.categoria AS CATEGORIA_PRODUTO COMMENT = 'Categoria do produto no ranking',
    top.ranking AS RANKING COMMENT = 'Posicao no ranking de vendas',
    infl.mes AS MES_INFLACAO COMMENT = 'Mes de referencia para inflacao',
    infl.indicador AS INDICADOR_CPI COMMENT = 'Nome do indicador de inflacao alimentar'
  )
  METRICS (
    kpi.receita_diaria AS SUM(kpi.receita_diaria) COMMENT = 'Receita total de vendas em EUR',
    kpi.ticket_medio AS AVG(kpi.ticket_medio) COMMENT = 'Valor medio por transacao em EUR',
    kpi.numero_transacoes AS SUM(kpi.numero_transacoes) COMMENT = 'Numero total de transacoes',
    cat.receita_mensal AS SUM(cat.receita_mensal) COMMENT = 'Receita mensal por categoria em EUR',
    cat.quantidade_total AS SUM(cat.quantidade_total) COMMENT = 'Quantidade total vendida',
    top.receita_total AS SUM(top.receita_total) COMMENT = 'Receita total do produto em EUR',
    top.margem_lucro_pct AS AVG(top.margem_lucro_pct) COMMENT = 'Margem de lucro percentual',
    infl.valor_indice AS AVG(infl.valor_indice) COMMENT = 'Indice de precos ao consumidor (CPI) base 2015=100',
    infl.receita_mensal AS SUM(infl.receita_mensal) COMMENT = 'Receita mensal do supermercado comparada com CPI'
  )
  COMMENT = 'Modelo semantico para analise de vendas SuperNova - inclui KPIs, categorias, produtos e inflacao';

-- =============================================================================
-- PARTE 2: Criar Cortex Search Service para reviews
-- =============================================================================

CREATE OR REPLACE CORTEX SEARCH SERVICE SUPERNOVA_LAB.GOLD.REVIEWS_SEARCH
  ON COMENTARIO
  ATTRIBUTES NOME_PRODUTO, CATEGORIA, RATING
  WAREHOUSE = SUPERNOVA_WH
  TARGET_LAG = '1 hour'
AS (
  SELECT 
    r.COMENTARIO,
    p.NOME_PRODUTO,
    p.CATEGORIA,
    r.RATING
  FROM SUPERNOVA_LAB.BRONZE.REVIEWS_PRODUTOS r
  JOIN SUPERNOVA_LAB.BRONZE.PRODUTOS p ON r.PRODUTO_ID = p.PRODUTO_ID
);

-- =============================================================================
-- PARTE 3: Criar o Cortex Agent - Analista SuperNova
-- =============================================================================

CREATE OR REPLACE AGENT SUPERNOVA_LAB.GOLD.ANALISTA_SUPERNOVA
  COMMENT = 'Analista de vendas inteligente para SuperNova Supermercados'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  orchestration:
    budget:
      seconds: 30
      tokens: 16000

  instructions:
    system: "Tu es um analista de dados especializado para a cadeia de supermercados SuperNova em Portugal. Ajudas gestores de loja e diretores a compreender performance de vendas, impacto da inflacao e feedback de clientes."
    orchestration: "Usa a ferramenta vendas_analyst para perguntas sobre receitas, KPIs, categorias, lojas, tendencias e inflacao. Usa a ferramenta feedback_search para perguntas sobre opiniao de clientes, qualidade de produtos e reclamacoes."
    response: "Responde sempre em Portugues de Portugal. Se conciso e inclui numeros concretos. Usa EUR para valores monetarios. Sugere acoes quando relevante."
    sample_questions:
      - question: "Qual a loja com mais vendas?"
        answer: "Vou consultar os dados de receita por loja para identificar a que tem melhor performance."
      - question: "O que dizem os clientes sobre frescos?"
        answer: "Vou pesquisar nas avaliacoes de clientes sobre produtos da categoria Frescos."
      - question: "A inflacao afetou as vendas?"
        answer: "Vou analisar a correlacao entre o indice CPI alimentar e a receita mensal."

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "vendas_analyst"
        description: "Analisa dados estruturados de vendas: receitas, KPIs, categorias de produtos, performance por loja, tendencias mensais e diarias, e impacto da inflacao. Usar para perguntas sobre numeros, rankings e metricas de negocio."
    - tool_spec:
        type: "cortex_search"
        name: "feedback_search"
        description: "Pesquisa avaliacoes e comentarios de clientes sobre produtos. Usar para perguntas sobre satisfacao, reclamacoes, qualidade percebida e opiniao dos consumidores."
    - tool_spec:
        type: "data_to_chart"
        name: "data_to_chart"
        description: "Gera graficos e visualizacoes a partir dos dados."

  tool_resources:
    vendas_analyst:
      semantic_view: "SUPERNOVA_LAB.GOLD.SV_SUPERNOVA"
    feedback_search:
      name: "SUPERNOVA_LAB.GOLD.REVIEWS_SEARCH"
      max_results: "5"
      title_column: "NOME_PRODUTO"
  $$;

-- =============================================================================
-- VERIFICACAO
-- =============================================================================

SHOW SEMANTIC VIEWS IN SCHEMA GOLD;
SHOW CORTEX SEARCH SERVICES IN SCHEMA GOLD;
SHOW AGENTS IN SCHEMA GOLD;

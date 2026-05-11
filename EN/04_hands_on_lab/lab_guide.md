# Hands-On Lab: SuperNova Supermarkets

> **Duration:** ~30 minutes
> **Format:** Guided exercise with AI prompts
> **Scenario:** Build the analytics platform of a Portuguese supermarket on Snowflake
> **Requirements:** Snowflake account (trial or demo) with ACCOUNTADMIN role + Cortex Code

---

## Scenario

**SuperNova** is a Portuguese supermarket chain with 12 stores spread across Portugal. Your goal is to build the complete data platform: from raw data ingestion to an intelligent assistant that answers questions in natural language.

**What we will build in 30 minutes:**

| Step | What we do | Tool | Time |
|------|------------|------|------|
| 1 | Load data into the Bronze layer | SQL Script | 5 min |
| 2 | Create Silver and Gold layers | dbt Project (Cortex Code) | 8 min |
| 3 | Create interactive dashboard | Streamlit (Cortex Code) | 8 min |
| 4 | Create sales assistant | Cortex Agent (Cortex Code) | 9 min |

---

## Prerequisites

- [ ] Browser open at **https://app.snowflake.com**
- [ ] Logged into your account
- [ ] **ACCOUNTADMIN** role selected (bottom left corner)
- [ ] **Cortex Code** open (desktop application)
- [ ] Confirm access to the Marketplace: **Data Products > Marketplace** (side menu)

---

## Step 1: Get Data from the Marketplace + Load Bronze (5 min)

### 1a. Get data from the Snowflake Marketplace

We will get **real** economic indicator data to enrich our analysis.

**Step-by-step instructions:**

1. In the Snowsight side menu, click on **Data Products > Marketplace**
2. In the search bar, search for: **"Financial & Economic Essentials"** (provider: Cybersyn)
3. Click on the listing **"Financial & Economic Essentials"**
4. Click the **"Get"** button (top right corner)
5. In the dialog:
   - **Database name:** keep `FINANCE__ECONOMICS` (or the suggested name)
   - **Roles:** select `ACCOUNTADMIN`
6. Click **"Get"**
7. Wait for confirmation: "Database created successfully"

> **What did we just do?** We obtained real data from the European Central Bank (ECB) about consumer price indices in Portugal. This data is shared in real time - no copies, no ETL!

**Note:** If you already have this dataset in your account (check in Databases > FINANCE__ECONOMICS), you can skip this sub-step.

### 1b. Run the Bronze setup script

1. Open a **SQL Worksheet**: click `+` > SQL Worksheet
2. Name it: "SuperNova - Setup Bronze"
3. Copy and paste **all** the content from the `setup_bronze.sql` file
4. Run everything: **Ctrl+Shift+Enter** (or click "Run All")

**Expected result (last query):**
```
| LOJAS | PRODUTOS | CLIENTES | VENDAS | REVIEWS |
|-------|----------|----------|--------|---------|
|    12 |       42 |       20 |   3000 |      20 |
```

> **Key concept:** The Bronze layer contains internal data in its raw state. The inflation data (CPI) comes directly from the Marketplace — in the next step, dbt will consume it without any copying!

---

## Step 2: Create Silver and Gold Layers with dbt Project (8 min)

Now we will use **Cortex Code** to automatically create a dbt project that transforms raw data into analytical tables ready for consumption.

### 2a. Open Cortex Code and paste the prompt

In the Cortex Code chat, paste:

```
Cria um dbt project chamado SUPERNOVA_TRANSFORMS para o supermercado SuperNova.
O projeto deve transformar os dados brutos da base SUPERNOVA_LAB.BRONZE em
tabelas analiticas organizadas em duas camadas:

Camada Silver (dados enriquecidos):
- Uma tabela VENDAS_ENRIQUECIDAS com informacao completa de cada venda (juntando produto, loja e cliente)
- Uma tabela CLIENTES_360 com visao unica de cada cliente (total gasto, numero de compras, ticket medio)

Camada Gold (metricas de negocio prontas para dashboards):
- KPI_DIARIO: receita diaria, numero de transacoes e ticket medio por loja
- VENDAS_CATEGORIA_MENSAL: receita mensal por categoria de produto
- TOP_PRODUTOS: ranking dos produtos mais vendidos com margem de lucro
- INFLACAO_VS_VENDAS: comparacao mensal entre o indice de inflacao alimentar (CPI)
  e a receita mensal do supermercado, para analise de correlacao precos vs vendas

As tabelas fonte internas sao: SUPERNOVA_LAB.BRONZE.VENDAS, SUPERNOVA_LAB.BRONZE.PRODUTOS,
SUPERNOVA_LAB.BRONZE.LOJAS e SUPERNOVA_LAB.BRONZE.CLIENTES.
Para o modelo de inflacao, usa diretamente os dados do Marketplace:
FINANCE__ECONOMICS.CYBERSYN.EUROPEAN_CENTRAL_BANK_TIMESERIES (filtrar por Portugal
e indicadores de CPI alimentar) juntando com FINANCE__ECONOMICS.CYBERSYN.GEOGRAPHY_INDEX.
O warehouse e SUPERNOVA_WH e o role e ACCOUNTADMIN.

Depois de criar o projeto, faz deploy e executa para materializar todas as tabelas.
```

### 2b. What happens

Cortex Code will automatically:
1. Create the dbt project structure with the 6 SQL models
2. Deploy the project to Snowflake as a `DBT PROJECT` object
3. Execute the models to create the Silver and Gold tables

**Expected result:** `PASS=6 WARN=0 ERROR=0`

> **Key concept:** With a single prompt in natural language, we created a complete data transformation pipeline — that consumes Marketplace data directly without copies! dbt combines internal data (Bronze) with external data (Marketplace) in a single Gold layer.

> **Note:** Since Cortex Code generates code dynamically, column names and structure may vary slightly. If the result is not PASS=6, check the Troubleshooting section at the end of this guide.

---

## Step 3: Create Interactive Dashboard with Streamlit (8 min)

We will create an executive panel for SuperNova's management to visualize KPIs in real time.

### 3a. Paste the following prompt in Cortex Code

```
Cria uma Streamlit app chamada SuperNova_CEO_Dashboard na base SUPERNOVA_LAB schema APPS
usando o warehouse SUPERNOVA_WH. A app deve ser o painel diario do CEO da cadeia de
supermercados SuperNova Portugal (12 lojas) com design profissional e executivo.

Fontes de dados (usa APENAS estas tabelas e colunas, nao inventes outras):

1. SUPERNOVA_LAB.GOLD.KPI_DIARIO
   Colunas: DATA_VENDA (date), LOJA_ID (number), NOME_LOJA (text),
   RECEITA_DIARIA (number), NUMERO_TRANSACOES (number), TICKET_MEDIO (number)

2. SUPERNOVA_LAB.GOLD.VENDAS_CATEGORIA_MENSAL
   Colunas: MES (date), CATEGORIA (text), RECEITA_MENSAL (number),
   QUANTIDADE_TOTAL (number), NUMERO_VENDAS (number)

3. SUPERNOVA_LAB.GOLD.TOP_PRODUTOS
   Colunas: PRODUTO_ID (number), NOME_PRODUTO (text), CATEGORIA (text),
   RECEITA_TOTAL (number), QUANTIDADE_VENDIDA (number), MARGEM_LUCRO_PCT (number),
   RANKING (number)

4. SUPERNOVA_LAB.GOLD.INFLACAO_VS_VENDAS
   (esta tabela foi criada pelo dbt no passo anterior - consulta as colunas reais
   com SELECT * LIMIT 1 antes de usar. Deve ter colunas de mes, indice CPI e receita)

Layout e conteudo:
1. Header com titulo "SuperNova" e subtitulo "Painel Estrategico" com estilo profissional
2. Sidebar com:
   - Filtro de periodo (selectbox com opcoes: Ultimo mes, Ultimos 3 meses, Todo o periodo)
   - Filtro de loja (selectbox com "Todas as lojas" + lista de NOME_LOJA)
3. Linha de KPIs com 4 metricas usando st.metric com deltas comparativos:
   - Receita Total (soma de RECEITA_DIARIA, comparar com periodo anterior)
   - Ticket Medio (media de TICKET_MEDIO)
   - Total Transacoes (soma de NUMERO_TRANSACOES)
   - Numero de Lojas Ativas
4. Duas colunas:
   - Esquerda: grafico de linhas com evolucao da RECEITA_DIARIA ao longo de DATA_VENDA
   - Direita: grafico de barras vertical com receita total por NOME_LOJA (ordenado desc)
5. Duas colunas:
   - Esquerda: grafico de barras com RECEITA_MENSAL por CATEGORIA
   - Direita: tabela com Top 10 produtos (RANKING, NOME_PRODUTO, CATEGORIA, RECEITA_TOTAL, MARGEM_LUCRO_PCT)
6. Seccao "Inflacao vs Vendas": grafico de linhas dual-axis com VALOR_INDICE (CPI) e RECEITA_MENSAL
   ao longo do MES (usando dados de INFLACAO_VS_VENDAS, filtrar INDICADOR = 'CPI_Alimentos_Geral')
7. Seccao final: tabela resumo por loja com NOME_LOJA, receita total, total transacoes, ticket medio

Regras tecnicas importantes:
- Usar get_active_session() para ligar ao Snowflake
- NAO usar hide_index em st.dataframe (nao e compativel)
- NAO usar st.container(border=True) (nao e compativel)
- NAO usar icones :material/ (nao e compativel)
- NAO usar horizontal=True em st.bar_chart (nao e compativel)
- NAO inventar colunas que nao existem nas tabelas acima
- Antes de escrever codigo, faz SELECT * LIMIT 1 em cada tabela para confirmar colunas
- Usar cores e formatacao para dar aspeto profissional (st.markdown com HTML inline)
```

### 3b. What happens

Cortex Code creates the Streamlit application directly in Snowflake. After it is created:

1. Go to **Projects > Streamlit** in Snowsight
2. Open **SuperNova_CEO_Dashboard**
3. The app shows metrics, charts, and tables in real time

> **Key concept:** An interactive app created in minutes with a simple prompt! Live data, governed by the same Snowflake permissions. No infrastructure, no external deployment.

---

## Step 4: Create Sales Assistant with Cortex Agent (9 min)

The final step: create an intelligent assistant that the management team can use to ask questions in natural language about sales and customer satisfaction.

### 4a. Paste the following prompt in Cortex Code

```
Cria um Cortex Agent chamado ANALISTA_SUPERNOVA na base SUPERNOVA_LAB schema GOLD
que funcione como analista de vendas inteligente para o supermercado SuperNova.

O agente deve ser capaz de:
- Responder perguntas sobre vendas, receitas, KPIs e rankings de produtos
  (usando os dados de SUPERNOVA_LAB.GOLD: KPI_DIARIO, VENDAS_CATEGORIA_MENSAL,
  TOP_PRODUTOS e INFLACAO_VS_VENDAS)
- Analisar a correlacao entre inflacao alimentar e vendas do supermercado
- Pesquisar avaliacoes e comentarios de clientes sobre produtos
  (usando SUPERNOVA_LAB.BRONZE.REVIEWS_PRODUTOS, coluna COMENTARIO)
- Gerar graficos quando relevante
- Responder sempre em Portugues

Cria toda a infraestrutura necessaria: Semantic View para os dados estruturados
e Cortex Search Service para as reviews. O warehouse e SUPERNOVA_WH.
```

### 4b. Test the Agent

After it is created:

1. In the side menu: **AI & ML > Agents** (or **Snowflake Intelligence**)
2. Select: **ANALISTA_SUPERNOVA**
3. Ask questions in natural language:

**Suggested test questions:**

| Question | What the Agent does |
|----------|---------------------|
| "Qual a loja com mais receita?" | Queries sales data (Cortex Analyst) |
| "O que dizem os clientes sobre o bacalhau?" | Searches reviews (Cortex Search) |
| "Top 5 produtos por vendas" | Generates table with ranking |
| "Mostra a receita por mes num grafico" | Generates visualization |
| "A inflacao afetou as nossas vendas?" | Analyzes CPI vs revenue correlation |
| "Quais produtos tem piores avaliacoes?" | Searches reviews with low ratings |

> **Key concept:** The Agent decides on its own which tool to use! Business users ask questions in natural language — no SQL, no code, no complexity.

---

## Congratulations!

You have successfully completed the lab. In 30 minutes:

- **Integrated** real data from the Snowflake Marketplace (ECB CPI Portugal)
- **Built** a medallion architecture (Bronze > Silver > Gold) with dbt Projects on Snowflake via Cortex Code
- **Created** an interactive dashboard with Streamlit in Snowflake
- **Implemented** an intelligent assistant with Cortex Agent

### Final Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPERNOVA_LAB                                  │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│    BRONZE    │    SILVER    │     GOLD     │       APPS        │
│              │              │              │                   │
│ - Lojas      │ - Vendas     │ - KPI_Diario │ - Streamlit App   │
│ - Produtos   │   Enriquecidas│ - Vendas    │ - dbt Project     │
│ - Clientes   │ - Clientes   │   Categoria  │                   │
│ - Vendas     │   360        │ - Top        │   AI & ML:        │
│ - Reviews    │              │   Produtos   │ - Semantic View   │
│              │              │ - Inflacao   │ - Search Service  │
│              │              │   vs Vendas  │ - Cortex Agent    │
└──────────────┴──────────────┴──────┬───────┴───────────────────┘
                                     │
                    ┌────────────────┘
                    ▼
       ┌──────────────────────────┐
       │  FINANCE__ECONOMICS      │
       │  (Snowflake Marketplace) │
       │  CPI Portugal - ECB      │
       └──────────────────────────┘
```

### Everything created with 3 prompts in Cortex Code!

| Prompt | Result |
|--------|--------|
| Prompt 1 | dbt project with 6 models (Silver + Gold + Marketplace) |
| Prompt 2 | Interactive Streamlit dashboard with inflation analysis |
| Prompt 3 | Intelligent sales agent |

### Recommended next steps

1. **Dynamic Tables:** Convert Silver/Gold to Dynamic Tables for automatic refresh
2. **Masking Policies:** Protect customer emails and phone numbers
3. **Tasks:** Schedule dbt project execution with `CREATE TASK`
4. **Certification:** SnowPro Core at [learn.snowflake.com](https://learn.snowflake.com)

---

## Troubleshooting

### Step 1: Bronze Setup

| Problem | Cause | Solution |
|---------|-------|----------|
| "Database FINANCE__ECONOMICS does not exist" | Marketplace was not installed | Go back to step 1a and install "Financial & Economic Essentials" |
| "Run All" only shows one result | Snowsight only shows the last result | Normal — verify it shows 12/42/20/3000/20 |
| Numbers different from 3000 in VENDAS | Data is randomly generated | Normal — the important thing is that there are ~3000 rows |

### Step 2: dbt Project

| Problem | Cause | Solution |
|---------|-------|----------|
| Cortex Code creates schemas SILVER_SILVER / GOLD_GOLD | Missing generate_schema_name macro | Ask Cortex Code: "Add a generate_schema_name macro that uses custom_schema_name directly without prefix" |
| ERROR in the inflacao_vs_vendas model | Missing Marketplace access | Verify that FINANCE__ECONOMICS exists and the role has IMPORTED PRIVILEGES |
| "profiles.yml validation error" | Missing account/user | Ask Cortex Code: "In profiles.yml set account: placeholder and user: placeholder" |
| PASS=5 instead of PASS=6 | Missing inflation model | Verify that the prompt mentions INFLACAO_VS_VENDAS and FINANCE__ECONOMICS |

### Step 3: Streamlit Dashboard

| Problem | Cause | Solution |
|---------|-------|----------|
| KeyError: column does not exist (e.g.: CIDADE_LOJA) | Cortex Code made up column names | Tell Cortex Code: "Fix the error: use only the columns listed in the original prompt" |
| TypeError: hide_index | SiS version does not support this parameter | Tell Cortex Code: "Remove hide_index from all st.dataframe" |
| TypeError: unexpected argument 'horizontal' | st.bar_chart does not support horizontal in this version | Tell Cortex Code: "Remove horizontal=True from bar_chart, use vertical bars" |
| st.container(border=True) error | SiS version does not support this parameter | Tell Cortex Code: "Remove border=True from st.container" |
| INFLACAO_VS_VENDAS columns different from prompt | dbt generated different names | Tell Cortex Code: "Run SELECT * FROM SUPERNOVA_LAB.GOLD.INFLACAO_VS_VENDAS LIMIT 1 and adapt the code" |
| App does not appear in Projects > Streamlit | App created in another schema | Check if it is in SUPERNOVA_LAB.APPS |

### Step 4: Cortex Agent

| Problem | Cause | Solution |
|---------|-------|----------|
| Semantic View syntax error | Complex syntax | Ask Cortex Code to recreate. Verify: DIMENSIONS before METRICS |
| Agent does not respond about inflation | Semantic View does not include INFLACAO_VS_VENDAS | Ask Cortex Code: "Add the INFLACAO_VS_VENDAS table to the Semantic View" |
| Search does not find reviews | Cortex Search still indexing | Wait 1-2 minutes after creation |
| "Agent not found" in Snowsight | May be in another schema | Check in AI & ML > Agents, filter by SUPERNOVA_LAB.GOLD |

### General tip

If Cortex Code generates an error, just tell it:
> "Fix the previous error: [paste error message]"

The assistant automatically fixes it in most cases!

---

## Cleanup (Optional)

```sql
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS SUPERNOVA_LAB;
DROP WAREHOUSE IF EXISTS SUPERNOVA_WH;
```

---

*SuperNova Supermarkets - Lab built for Snowflake Partner Enablement, Lisbon 2026*

# Laboratorio Pratico: SuperNova Supermercados

> **Duracao:** ~30 minutos
> **Formato:** Exercicio guiado com prompts de IA
> **Cenario:** Construir a plataforma analitica de um supermercado portugues no Snowflake
> **Requisitos:** Conta Snowflake (trial ou demo) com role ACCOUNTADMIN + Cortex Code

---

## Cenario

A **SuperNova** e uma cadeia de supermercados portuguesa com 12 lojas espalhadas por Portugal. O vosso objetivo e construir a plataforma de dados completa: desde a ingestao de dados brutos ate um assistente inteligente que responde a perguntas em linguagem natural.

**O que vamos construir em 30 minutos:**

| Passo | O que fazemos | Ferramenta | Tempo |
|-------|--------------|------------|-------|
| 1 | Carregar dados na camada Bronze | SQL Script | 5 min |
| 2 | Criar camadas Silver e Gold | dbt Project (Cortex Code) | 8 min |
| 3 | Criar super app multi-pagina | Streamlit (Cortex Code) | 8 min |
| 4 | Criar assistente de vendas | Cortex Agent (Cortex Code) | 9 min |

---

## Pre-requisitos

- [ ] Browser aberto em **https://app.snowflake.com**
- [ ] Sessao iniciada na vossa conta
- [ ] Role **ACCOUNTADMIN** selecionado (canto inferior esquerdo)
- [ ] **Cortex Code** aberto (aplicacao desktop)

---

## Passo 1: Carregar Dados na Camada Bronze (5 min)

### 1a. Executar o script de setup Bronze

1. Abrir uma **SQL Worksheet**: clicar `+` > SQL Worksheet
2. Dar o nome: "SuperNova - Setup Bronze"
3. Copiar e colar **todo** o conteudo do ficheiro `setup_bronze.sql`
4. Executar tudo: **Ctrl+Shift+Enter** (ou clicar "Run All")

**Resultado esperado (ultima query):**
```
| LOJAS | PRODUTOS | CLIENTES | VENDAS | REVIEWS |
|-------|----------|----------|--------|---------|
|    12 |       42 |       20 |   3000 |      20 |
```

> **Conceito-chave:** A camada Bronze contem dados internos em estado bruto — os dados transacionais do supermercado que alimentam toda a plataforma analitica.

---

## Passo 2: Criar Camadas Silver e Gold com dbt Project (8 min)

Agora vamos usar o **Cortex Code** para criar automaticamente um projeto dbt que transforma os dados brutos em tabelas analiticas prontas para consumo.

### 2a. Abrir o Cortex Code e colar o prompt

No chat do Cortex Code, colar:

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

As tabelas fonte internas sao: SUPERNOVA_LAB.BRONZE.VENDAS, SUPERNOVA_LAB.BRONZE.PRODUTOS,
SUPERNOVA_LAB.BRONZE.LOJAS e SUPERNOVA_LAB.BRONZE.CLIENTES.
O warehouse e SUPERNOVA_WH e o role e ACCOUNTADMIN.

Depois de criar o projeto, faz deploy e executa para materializar todas as tabelas.
```

### 2b. O que acontece

O Cortex Code vai automaticamente:
1. Criar a estrutura do projeto dbt com os 5 modelos SQL
2. Desplegar o projeto no Snowflake como objecto `DBT PROJECT`
3. Executar os modelos para criar as tabelas Silver e Gold

**Resultado esperado:** `PASS=5 WARN=0 ERROR=0`

> **Conceito-chave:** Com um unico prompt em linguagem natural, criamos um pipeline de transformacao de dados completo com 5 modelos! O dbt organiza a transformacao de dados brutos (Bronze) em tabelas analiticas prontas para consumo (Silver e Gold).

> **Nota:** Como o Cortex Code gera codigo dinamicamente, os nomes de colunas e a estrutura podem variar ligeiramente. Se o resultado nao for PASS=5, consultem a seccao de Troubleshooting no final desta guia.

---

## Passo 3: Criar Dashboard Interativo com Streamlit (8 min)

Vamos criar um painel executivo para a direcao do SuperNova visualizar os KPIs em tempo real — diretamente dentro do Snowflake.

> **Importante:** Como o Cortex Code gera os modelos dbt dinamicamente, os nomes das colunas podem variar. O prompt abaixo instrui o Cortex Code a **descobrir primeiro** as colunas reais antes de escrever o codigo.

### 3a. Colar o seguinte prompt no Cortex Code

```
Cria uma Streamlit app chamada SuperNova_Command_Center na base SUPERNOVA_LAB schema APPS
usando o warehouse SUPERNOVA_WH. A app deve ser desplegada como um objecto Streamlit in
Snowflake (usando CREATE STREAMLIT) para que apareca na seccao Projects > Streamlit Apps
do Snowsight. Tudo num unico ficheiro streamlit_app.py.

PASSO OBRIGATORIO ANTES DE ESCREVER CODIGO:
Executa SELECT * FROM <tabela> LIMIT 5 nas seguintes 3 tabelas Gold para descobrir
os nomes REAIS das colunas (podem variar porque foram geradas por dbt no passo anterior):
- SUPERNOVA_LAB.GOLD.KPI_DIARIO (deve ter colunas de: data, loja, receita diaria, transacoes, ticket medio)
- SUPERNOVA_LAB.GOLD.VENDAS_CATEGORIA_MENSAL (deve ter colunas de: mes, categoria, receita mensal, quantidade, numero vendas)
- SUPERNOVA_LAB.GOLD.TOP_PRODUTOS (deve ter colunas de: produto, categoria, receita, quantidade, margem, ranking)
Usa os nomes EXATOS que encontrares nos resultados. NAO assumes nomes fixos.

A app deve ser o painel de comando do CEO da cadeia de supermercados SuperNova Portugal
(12 lojas) com design profissional. Usa st.tabs para organizar em 4 seccoes:

TAB 1 - "Visao Geral":
- Header com titulo "SuperNova Command Center" usando st.markdown com HTML e gradiente azul
- Sidebar com filtro de periodo (selectbox: Ultimo mes, Ultimos 3 meses, Todo o periodo)
  e filtro de loja (selectbox: "Todas as lojas" + lista de lojas)
- Linha de 4 KPIs com st.metric: Receita Total, Ticket Medio, Total Transacoes, Lojas Ativas
- Duas colunas: grafico de linhas (receita diaria ao longo do tempo) e barras (receita por loja)

TAB 2 - "Analise de Categorias":
- Grafico de barras com receita mensal por categoria
- Tabela com evolucao mensal por categoria
- Metricas resumo: categoria com mais receita, categoria com mais crescimento

TAB 3 - "Top Produtos":
- Tabela com Top 10 produtos (ranking, nome, categoria, receita, margem)
- Grafico de barras com os top 10 por receita
- Metricas: produto com melhor margem, produto mais vendido

TAB 4 - "Desempenho por Loja":
- Tabela resumo por loja: nome, receita total, total transacoes, ticket medio
- Grafico de barras comparando receita por loja
- Ranking visual das lojas com barras de progresso em HTML

Regras tecnicas CRITICAS:
- Usar get_active_session() para ligar ao Snowflake (NAO usar st.connection)
- Tudo num UNICO ficheiro streamlit_app.py (sem ficheiros separados, sem pastas pages/)
- Desplegar como objecto Streamlit in Snowflake com CREATE STREAMLIT
- NAO usar hide_index em st.dataframe (nao e compativel com SiS)
- NAO usar st.container(border=True) (nao e compativel com SiS)
- NAO usar icones :material/ (nao e compativel com SiS)
- NAO usar horizontal=True em st.bar_chart (nao e compativel com SiS)
- NAO usar st.navigation nem st.Page (nao e compativel com SiS warehouse mode)
- Tratar valores NaN/None antes de converter para int (usar fillna(0))
- Usar cores Snowflake (#29B5E8, #11567F, #7D44CF, #FF9F36) e st.markdown HTML para estilo
```

### 3b. O que acontece

O Cortex Code primeiro inspecciona as tabelas Gold para descobrir as colunas reais, e depois cria a aplicacao Streamlit. Depois de criada:

1. Ir a **Projects > Streamlit** no Snowsight
2. Abrir **SuperNova_Command_Center**
3. A app mostra 4 tabs com metricas, graficos e tabelas em tempo real

> **Conceito-chave:** Uma app interativa criada em minutos com um simples prompt! Dados ao vivo, governada pelas mesmas permissoes do Snowflake. Sem infraestrutura, sem deploy externo — a app vive diretamente dentro do Snowflake.

---

## Passo 4: Criar Assistente de Vendas com Cortex Agent (9 min)

O passo final: criar um assistente inteligente que a equipa de gestao pode usar para fazer perguntas em linguagem natural sobre as vendas e a satisfacao dos clientes.

### 4a. Colar o seguinte prompt no Cortex Code

```
Cria um Cortex Agent chamado ANALISTA_SUPERNOVA na base SUPERNOVA_LAB schema GOLD
que funcione como analista de vendas inteligente para o supermercado SuperNova.

PASSO OBRIGATORIO ANTES DE CRIAR O AGENT:
Executa SELECT * FROM <tabela> LIMIT 5 nas seguintes tabelas para descobrir
os nomes REAIS das colunas (podem variar porque foram geradas por dbt):
- SUPERNOVA_LAB.GOLD.KPI_DIARIO
- SUPERNOVA_LAB.GOLD.VENDAS_CATEGORIA_MENSAL
- SUPERNOVA_LAB.GOLD.TOP_PRODUTOS
- SUPERNOVA_LAB.BRONZE.REVIEWS_PRODUTOS
Usa os nomes EXATOS que encontrares para criar a Semantic View e o Search Service.

O agente deve ser capaz de:
- Responder perguntas sobre vendas, receitas, KPIs e rankings de produtos
  (usando os dados das tabelas GOLD que descobriste acima)
- Pesquisar avaliacoes e comentarios de clientes sobre produtos
  (usando SUPERNOVA_LAB.BRONZE.REVIEWS_PRODUTOS, coluna de comentarios/texto)
- Gerar graficos quando relevante
- Responder sempre em Portugues

Cria toda a infraestrutura necessaria: Semantic View para os dados estruturados
e Cortex Search Service para as reviews. O warehouse e SUPERNOVA_WH.
```

### 4b. Testar o Agent

Depois de criado:

1. No menu lateral: **AI & ML > Agents** (ou **Snowflake Intelligence**)
2. Selecionar: **ANALISTA_SUPERNOVA**
3. Fazer perguntas em linguagem natural:

**Perguntas de teste sugeridas:**

| Pergunta | O que o Agent faz |
|----------|-------------------|
| "Qual a loja com mais receita?" | Consulta dados de vendas (Cortex Analyst) |
| "O que dizem os clientes sobre o bacalhau?" | Pesquisa nas reviews (Cortex Search) |
| "Top 5 produtos por vendas" | Gera tabela com ranking |
| "Mostra a receita por mes num grafico" | Gera visualizacao |
| "Quais produtos tem piores avaliacoes?" | Pesquisa reviews com rating baixo |

> **Conceito-chave:** O Agent decide sozinho qual ferramenta usar! Utilizadores de negocio fazem perguntas em linguagem natural — sem SQL, sem codigo, sem complexidade.

---

## Parabens!

Completaram o laboratorio com sucesso. Em 30 minutos:

- **Carregaram** dados transacionais na camada Bronze
- **Construiram** uma arquitetura medallion (Bronze > Silver > Gold) com dbt Projects on Snowflake via Cortex Code
- **Criaram** uma super app multi-pagina com Streamlit in Snowflake
- **Implementaram** um assistente inteligente com Cortex Agent

### Arquitetura Final

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPERNOVA_LAB                                  │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│    BRONZE    │    SILVER    │     GOLD     │       APPS        │
│              │              │              │                   │
│ - Lojas      │ - Vendas     │ - KPI_Diario │ - Streamlit App   │
│ - Produtos   │   Enriquecidas│ - Vendas    │   (4 paginas)     │
│ - Clientes   │ - Clientes   │   Categoria  │ - dbt Project     │
│ - Vendas     │   360        │ - Top        │                   │
│ - Reviews    │              │   Produtos   │   AI & ML:        │
│              │              │              │ - Semantic View   │
│              │              │              │ - Search Service  │
│              │              │              │ - Cortex Agent    │
└──────────────┴──────────────┴──────┬───────┴───────────────────┘

      
```

### Tudo criado com 3 prompts no Cortex Code!

| Prompt | Resultado |
|--------|-----------|
| Prompt 1 | Projeto dbt com 5 modelos (Silver + Gold) |
| Prompt 2 | Super app Streamlit multi-pagina (4 paginas) |
| Prompt 3 | Agente inteligente de vendas |

### Proximos passos recomendados

1. **Dynamic Tables:** Converter Silver/Gold em Dynamic Tables para refresh automatico
2. **Masking Policies:** Proteger emails e telefones dos clientes
3. **Tasks:** Agendar execucao do dbt project com `CREATE TASK`
4. **Certificacao:** SnowPro Core em [learn.snowflake.com](https://learn.snowflake.com)

---

## Resolucao de Problemas (Troubleshooting)

### Passo 1: Setup Bronze

| Problema | Causa | Solucao |
|----------|-------|---------|
| "Run All" so mostra um resultado | Snowsight mostra apenas o ultimo resultado | Normal — verificar que mostra 12/42/20/3000/20 |
| Numeros diferentes de 3000 em VENDAS | Dados sao gerados aleatoriamente | Normal — o importante e que haja ~3000 rows |

### Passo 2: dbt Project

| Problema | Causa | Solucao |
|----------|-------|---------|
| Cortex Code cria schemas SILVER_SILVER / GOLD_GOLD | Falta macro generate_schema_name | Pedir ao Cortex Code: "Adiciona um macro generate_schema_name que use custom_schema_name diretamente sem prefixo" |
| "profiles.yml validation error" | Falta account/user | Pedir ao Cortex Code: "No profiles.yml coloca account: placeholder e user: placeholder" |
| PASS=4 em vez de PASS=5 | Falta um modelo | Verificar que o prompt menciona os 5 modelos: VENDAS_ENRIQUECIDAS, CLIENTES_360, KPI_DIARIO, VENDAS_CATEGORIA_MENSAL, TOP_PRODUTOS |

### Passo 3: Streamlit Dashboard

| Problema | Causa | Solucao |
|----------|-------|---------|
| KeyError: coluna nao existe | Cortex Code nao inspeccionou as tabelas antes | Dizer ao Cortex Code: "Faz SELECT * LIMIT 5 em cada tabela Gold e adapta o codigo as colunas reais" |
| ValueError: cannot convert NaN | Valores nulos nos dados | Dizer ao Cortex Code: "Adiciona .fillna(0) antes de converter para int" |
| TypeError: hide_index | Versao SiS nao suporta este parametro | Dizer ao Cortex Code: "Remove hide_index de todos os st.dataframe" |
| TypeError: unexpected argument 'horizontal' | st.bar_chart nao suporta horizontal | Dizer ao Cortex Code: "Remove horizontal=True do bar_chart, usa barras verticais" |
| st.container(border=True) erro | Versao SiS nao suporta | Dizer ao Cortex Code: "Remove border=True de st.container" |
| App nao aparece em Projects > Streamlit | App criada noutro schema ou nao desplegada | Verificar se esta em SUPERNOVA_LAB.APPS. Se nao, pedir: "Desplega a app com CREATE STREAMLIT" |

### Passo 4: Cortex Agent

| Problema | Causa | Solucao |
|----------|-------|---------|
| Semantic View erro de sintaxe | Sintaxe complexa | Pedir ao Cortex Code para recriar. Verificar: DIMENSIONS antes de METRICS |
| Search nao encontra reviews | Cortex Search ainda a indexar | Aguardar 1-2 minutos apos criacao |
| "Agent not found" no Snowsight | Pode estar noutro schema | Verificar em AI & ML > Agents, filtrar por SUPERNOVA_LAB.GOLD |

### Dica geral

Se o Cortex Code gerar um erro, basta dizer-lhe:
> "Corrige o erro anterior: [colar mensagem de erro]"

O assistente corrige automaticamente na maioria dos casos!

---

## Limpeza (Opcional)

```sql
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS SUPERNOVA_LAB;
DROP WAREHOUSE IF EXISTS SUPERNOVA_WH;
```

---

*SuperNova Supermercados - Laboratorio construido para Snowflake Partner Enablement, Lisboa 2026*

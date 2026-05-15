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

## Passo 3: Criar Super App Multi-Pagina com Streamlit (8 min)

Vamos criar uma aplicacao profissional multi-pagina que serve como centro de comando para a direcao do SuperNova.

### 3a. Colar o seguinte prompt no Cortex Code

```
Cria uma Streamlit app multi-pagina chamada SuperNova_Command_Center na base SUPERNOVA_LAB
schema APPS usando o warehouse SUPERNOVA_WH. A app deve ser o centro de comando do CEO da
cadeia de supermercados SuperNova Portugal (12 lojas) com design profissional e executivo.

A app deve ter navegacao por paginas na sidebar (usando st.navigation e st.Page) com 4 paginas:

PAGINA 1 - "Visao Geral" (pagina principal):
- Header com titulo "SuperNova Command Center" e subtitulo "Centro de Comando Executivo"
- Sidebar com filtro de periodo (selectbox: Ultimo mes, Ultimos 3 meses, Todo o periodo)
  e filtro de loja (selectbox: "Todas as lojas" + lista de NOME_LOJA)
- Linha de 4 KPIs com st.metric: Receita Total, Ticket Medio, Total Transacoes, Lojas Ativas
- Duas colunas: grafico de linhas (receita diaria ao longo do tempo) e barras (receita por loja)

PAGINA 2 - "Analise de Categorias":
- Grafico de barras com RECEITA_MENSAL por CATEGORIA
- Tabela com evolucao mensal por categoria (pivot ou tabela detalhada)
- Metricas resumo: categoria com mais receita, categoria com mais crescimento

PAGINA 3 - "Top Produtos":
- Tabela interativa com Top 10 produtos (RANKING, NOME_PRODUTO, CATEGORIA, RECEITA_TOTAL, MARGEM_LUCRO_PCT)
- Grafico de barras horizontais com os top 10 por receita
- Metricas: produto com melhor margem, produto mais vendido

PAGINA 4 - "Desempenho por Loja":
- Tabela resumo por loja: NOME_LOJA, receita total, total transacoes, ticket medio
- Grafico de barras comparando receita por loja
- Mapa de calor ou ranking visual das lojas

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

Regras tecnicas importantes:
- Usar get_active_session() para ligar ao Snowflake
- NAO usar hide_index em st.dataframe (nao e compativel)
- NAO usar st.container(border=True) (nao e compativel)
- NAO usar icones :material/ (nao e compativel)
- NAO usar horizontal=True em st.bar_chart (nao e compativel)
- NAO inventar colunas que nao existem nas tabelas acima
- Antes de escrever codigo, faz SELECT * LIMIT 1 em cada tabela para confirmar colunas
- Usar cores e formatacao para dar aspeto profissional (st.markdown com HTML inline)
- Cada pagina deve ser um ficheiro separado na pasta pages/
```

### 3b. O que acontece

O Cortex Code cria a aplicacao Streamlit multi-pagina diretamente no Snowflake. Depois de criada:

1. Ir a **Projects > Streamlit** no Snowsight
2. Abrir **SuperNova_Command_Center**
3. A app mostra 4 paginas navegaveis com metricas, graficos e tabelas em tempo real

> **Conceito-chave:** Uma super app multi-pagina criada em minutos com um simples prompt! Quatro paginas de analise interativa, dados ao vivo, governada pelas mesmas permissoes do Snowflake. Sem infraestrutura, sem deploy externo.

---

## Passo 4: Criar Assistente de Vendas com Cortex Agent (9 min)

O passo final: criar um assistente inteligente que a equipa de gestao pode usar para fazer perguntas em linguagem natural sobre as vendas e a satisfacao dos clientes.

### 4a. Colar o seguinte prompt no Cortex Code

```
Cria um Cortex Agent chamado ANALISTA_SUPERNOVA na base SUPERNOVA_LAB schema GOLD
que funcione como analista de vendas inteligente para o supermercado SuperNova.

O agente deve ser capaz de:
- Responder perguntas sobre vendas, receitas, KPIs e rankings de produtos
  (usando os dados de SUPERNOVA_LAB.GOLD: KPI_DIARIO, VENDAS_CATEGORIA_MENSAL,
  TOP_PRODUTOS )
- Pesquisar avaliacoes e comentarios de clientes sobre produtos
  (usando SUPERNOVA_LAB.BRONZE.REVIEWS_PRODUTOS, coluna COMENTARIO)
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

### Passo 3: Streamlit Super App

| Problema | Causa | Solucao |
|----------|-------|---------|
| KeyError: coluna nao existe (ex: CIDADE_LOJA) | Cortex Code inventou nomes de colunas | Dizer ao Cortex Code: "Corrige o erro: usa apenas as colunas listadas no prompt original" |
| TypeError: hide_index | Versao SiS nao suporta este parametro | Dizer ao Cortex Code: "Remove hide_index de todos os st.dataframe" |
| TypeError: unexpected argument 'horizontal' | st.bar_chart nao suporta horizontal nesta versao | Dizer ao Cortex Code: "Remove horizontal=True do bar_chart, usa barras verticais" |
| st.container(border=True) erro | Versao SiS nao suporta este parametro | Dizer ao Cortex Code: "Remove border=True de st.container" |
| App nao aparece em Projects > Streamlit | App criada noutro schema | Verificar se esta em SUPERNOVA_LAB.APPS |
| Navegacao nao funciona | st.navigation nao disponivel | Pedir ao Cortex Code: "Usa st.sidebar.radio para navegacao entre paginas" |

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

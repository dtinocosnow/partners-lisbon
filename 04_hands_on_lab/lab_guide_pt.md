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
| 3 | Criar dashboard interativo | Streamlit (Cortex Code) | 8 min |
| 4 | Criar assistente de vendas | Cortex Agent (Cortex Code) | 9 min |

---

## Pre-requisitos

- [ ] Browser aberto em **https://app.snowflake.com**
- [ ] Sessao iniciada na vossa conta
- [ ] Role **ACCOUNTADMIN** selecionado (canto inferior esquerdo)
- [ ] **Cortex Code** aberto (aplicacao desktop)
- [ ] Confirmar acesso ao Marketplace: **Data Products > Marketplace** (menu lateral)

---

## Passo 1: Obter Dados do Marketplace + Carregar Bronze (5 min)

### 1a. Obter dados do Snowflake Marketplace

Vamos obter dados **reais** de indicadores economicos para enriquecer a nossa analise.

**Instrucoes passo a passo:**

1. No menu lateral do Snowsight, clicar em **Data Products > Marketplace**
2. Na barra de pesquisa, procurar: **"Financial & Economic Essentials"** (provider: Cybersyn)
3. Clicar no listing **"Financial & Economic Essentials"**
4. Clicar no botao **"Get"** (canto superior direito)
5. No dialogo:
   - **Database name:** manter `FINANCE__ECONOMICS` (ou o nome sugerido)
   - **Roles:** selecionar `ACCOUNTADMIN`
6. Clicar **"Get"**
7. Aguardar confirmacao: "Database created successfully"

> **O que acabamos de fazer?** Obtivemos dados reais do European Central Bank (ECB) sobre indices de precos ao consumidor em Portugal. Estes dados sao partilhados em tempo real - sem copias, sem ETL!

**Nota:** Se ja tiverem este dataset na conta (verificar em Databases > FINANCE__ECONOMICS), podem saltar este sub-passo.

### 1b. Executar o script de setup Bronze

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

> **Conceito-chave:** A camada Bronze contem dados internos em estado bruto. Os dados de inflacao (CPI) vem diretamente do Marketplace — no proximo passo, o dbt vai consumi-los sem qualquer copia!

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

### 2b. O que acontece

O Cortex Code vai automaticamente:
1. Criar a estrutura do projeto dbt com os 6 modelos SQL
2. Desplegar o projeto no Snowflake como objecto `DBT PROJECT`
3. Executar os modelos para criar as tabelas Silver e Gold

**Resultado esperado:** `PASS=6 WARN=0 ERROR=0`

> **Conceito-chave:** Com um unico prompt em linguagem natural, criamos um pipeline de transformacao de dados completo — que consome diretamente dados do Marketplace sem copias! O dbt combina dados internos (Bronze) com dados externos (Marketplace) numa unica camada Gold.

> **Nota:** Como o Cortex Code gera codigo dinamicamente, os nomes de colunas e a estrutura podem variar ligeiramente. Se o resultado nao for PASS=6, consultem a seccao de Troubleshooting no final desta guia.

---

## Passo 3: Criar Dashboard Interativo com Streamlit (8 min)

Vamos criar um painel executivo para a direcao do SuperNova visualizar os KPIs em tempo real.

### 3a. Colar o seguinte prompt no Cortex Code

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

### 3b. O que acontece

O Cortex Code cria a aplicacao Streamlit diretamente no Snowflake. Depois de criada:

1. Ir a **Projects > Streamlit** no Snowsight
2. Abrir **SuperNova_CEO_Dashboard**
3. A app mostra metricas, graficos e tabelas em tempo real

> **Conceito-chave:** Uma app interativa criada em minutos com um simples prompt! Dados ao vivo, governada pelas mesmas permissoes do Snowflake. Sem infraestrutura, sem deploy externo.

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
  TOP_PRODUTOS e INFLACAO_VS_VENDAS)
- Analisar a correlacao entre inflacao alimentar e vendas do supermercado
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
| "A inflacao afetou as nossas vendas?" | Analisa correlacao CPI vs receita |
| "Quais produtos tem piores avaliacoes?" | Pesquisa reviews com rating baixo |

> **Conceito-chave:** O Agent decide sozinho qual ferramenta usar! Utilizadores de negocio fazem perguntas em linguagem natural — sem SQL, sem codigo, sem complexidade.

---

## Parabens!

Completaram o laboratorio com sucesso. Em 30 minutos:

- **Integraram** dados reais do Snowflake Marketplace (ECB CPI Portugal)
- **Construiram** uma arquitetura medallion (Bronze > Silver > Gold) com dbt Projects on Snowflake via Cortex Code
- **Criaram** um dashboard interativo com Streamlit in Snowflake
- **Implementaram** um assistente inteligente com Cortex Agent

### Arquitetura Final

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

### Tudo criado com 3 prompts no Cortex Code!

| Prompt | Resultado |
|--------|-----------|
| Prompt 1 | Projeto dbt com 6 modelos (Silver + Gold + Marketplace) |
| Prompt 2 | Dashboard Streamlit interativo com analise de inflacao |
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
| "Database FINANCE__ECONOMICS does not exist" | Marketplace nao foi instalado | Voltar ao passo 1a e instalar "Financial & Economic Essentials" |
| "Run All" so mostra um resultado | Snowsight mostra apenas o ultimo resultado | Normal — verificar que mostra 12/42/20/3000/20 |
| Numeros diferentes de 3000 em VENDAS | Dados sao gerados aleatoriamente | Normal — o importante e que haja ~3000 rows |

### Passo 2: dbt Project

| Problema | Causa | Solucao |
|----------|-------|---------|
| Cortex Code cria schemas SILVER_SILVER / GOLD_GOLD | Falta macro generate_schema_name | Pedir ao Cortex Code: "Adiciona um macro generate_schema_name que use custom_schema_name diretamente sem prefixo" |
| ERROR no modelo inflacao_vs_vendas | Falta acesso ao Marketplace | Verificar que FINANCE__ECONOMICS existe e o role tem IMPORTED PRIVILEGES |
| "profiles.yml validation error" | Falta account/user | Pedir ao Cortex Code: "No profiles.yml coloca account: placeholder e user: placeholder" |
| PASS=5 em vez de PASS=6 | Falta modelo inflacao | Verificar que o prompt menciona INFLACAO_VS_VENDAS e FINANCE__ECONOMICS |

### Passo 3: Streamlit Dashboard

| Problema | Causa | Solucao |
|----------|-------|---------|
| KeyError: coluna nao existe (ex: CIDADE_LOJA) | Cortex Code inventou nomes de colunas | Dizer ao Cortex Code: "Corrige o erro: usa apenas as colunas listadas no prompt original" |
| TypeError: hide_index | Versao SiS nao suporta este parametro | Dizer ao Cortex Code: "Remove hide_index de todos os st.dataframe" |
| TypeError: unexpected argument 'horizontal' | st.bar_chart nao suporta horizontal nesta versao | Dizer ao Cortex Code: "Remove horizontal=True do bar_chart, usa barras verticais" |
| st.container(border=True) erro | Versao SiS nao suporta este parametro | Dizer ao Cortex Code: "Remove border=True de st.container" |
| Colunas INFLACAO_VS_VENDAS diferentes do prompt | dbt gerou nomes diferentes | Dizer ao Cortex Code: "Faz SELECT * FROM SUPERNOVA_LAB.GOLD.INFLACAO_VS_VENDAS LIMIT 1 e adapta o codigo" |
| App nao aparece em Projects > Streamlit | App criada noutro schema | Verificar se esta em SUPERNOVA_LAB.APPS |

### Passo 4: Cortex Agent

| Problema | Causa | Solucao |
|----------|-------|---------|
| Semantic View erro de sintaxe | Sintaxe complexa | Pedir ao Cortex Code para recriar. Verificar: DIMENSIONS antes de METRICS |
| Agent nao responde sobre inflacao | Semantic View nao inclui INFLACAO_VS_VENDAS | Pedir ao Cortex Code: "Adiciona a tabela INFLACAO_VS_VENDAS a Semantic View" |
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

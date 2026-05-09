# Snowflake AI Data Cloud — Partner Enablement Lisboa

Materiais para a sessao presencial de capacitacao tecnica de Partners em Lisboa, Portugal.

## Visao Geral

| | |
|---|---|
| **Duracao** | 3 horas |
| **Local** | Lisboa, Portugal |
| **Audiencia** | Data Analysts, Data Engineers, Architects |

### Oradores

- **Pedro Jose** — Visao estrategica e contexto de mercado | [LinkedIn](https://www.linkedin.com/in/pjose/)
- **David Tinoco** — Deep dives tecnicos e laboratorio pratico | [LinkedIn](https://www.linkedin.com/in/dtinocoreyes/)
- **Frederic Arendt** — Conclusao e Go-To-Market | [LinkedIn](https://www.linkedin.com/in/farendt/)

## Estrutura do Repositorio

```
partners-lisbon/
├── 01_agenda/                      # Agenda e one-pager da sessao
├── 03_demo_scripts/
│   ├── notebooks/                  # Notebooks interativas para demos ao vivo
│   │   ├── aprofundamento_I.ipynb      # Demo I: Setup, Data Loading, Snowpipe, Governance, Performance
│   │   └── aprofundamento_II.ipynb     # Demo II: Dynamic Tables, Cortex AI, Agent, Apps
│   ├── 00_setup_environment.sql    # Setup: DB, schemas, warehouses, roles
│   ├── 01_data_loading.sql         # Carga de dados (5 tabelas e-commerce)
│   ├── 01b_snowpipe_demo.sql       # Demo Snowpipe (ingestao continua)
│   ├── 02_governance_demo.sql      # Masking policies + Row access
│   ├── 03_performance_cost.sql     # Warehouse sizing, caching, resource monitors
│   ├── 04_dynamic_tables.sql       # Dynamic Tables (ETL declarativo)
│   ├── 05_cortex_ai_demo.sql       # Cortex AI: Sentiment, Translate, Semantic View
│   ├── 05b_cortex_agent_demo.sql   # Cortex Agent (Analyst + Search)
│   ├── 06_apps_marketplace.sql     # Secure views, cloning, tags
│   └── 99_cleanup.sql              # Limpeza completa do ambiente
├── 04_hands_on_lab/                # Laboratorio pratico SuperNova (guia + scripts)
├── 05_enablement/                  # Roadmap de capacitacao 60 dias
├── 06_resources/                   # Links e referencias uteis
└── 07_streamlit_app/               # Streamlit app (slides interativos) - deployed in Snowflake
    ├── streamlit_app.py                # Main app (multipage navigation)
    └── app_pages/                      # Paginas: agenda, deep_dive_1, deep_dive_2, lab_recursos
```

## Fluxo da Sessao

| Material | Formato | Descricao |
|----------|---------|-----------|
| **07_streamlit_app** | Streamlit in Snowflake | Explicacao teorica interativa (projetada) |
| **03_demo_scripts/notebooks** | Snowflake Workspace Notebooks | Demos ao vivo com codigo e visualizacoes |
| **04_hands_on_lab** | Guia markdown + SQL | Laboratorio pratico guiado (SuperNova) |
| **05_enablement** | Markdown | Percurso de capacitacao pos-sessao |
| **06_resources** | Markdown | Links, certificacoes, contactos |

## Agenda da Sessao

| Hora | Sessao | Orador | Material |
|------|--------|--------|----------|
| 10:00 | Boas-vindas e Objetivos | Pedro Jose | Streamlit |
| 10:10 | Visao Geral do Snowflake AI Data Cloud | Pedro Jose | Streamlit |
| 10:40 | Aprofundamento I: Fundamentos + Demo | David Tinoco | Streamlit + Notebook I |
| 11:15 | Intervalo | | |
| 11:25 | Aprofundamento II: IA e Aplicacoes + Demo | David Tinoco | Streamlit + Notebook II |
| 11:55 | Laboratorio Pratico Guiado | David Tinoco | Lab Guide |
| 12:25 | Pausa | | |
| 12:30 | Conclusao e Percurso de Capacitacao | Frederic Arendt | Streamlit |

## Temas Abordados

### Aprofundamento I — Fundamentos (Notebook I)
- Arquitectura multi-cluster de dados partilhados
- RBAC, Masking Policies, Row Access Policies
- Virtual Warehouses e elasticidade
- Camadas de cache e desempenho
- Snowpipe (ingestao continua)
- Dynamic Tables (ETL declarativo)

### Aprofundamento II — IA e Aplicacoes (Notebook II)
- Cortex AI: SENTIMENT, TRANSLATE, SUMMARIZE, CLASSIFY, COMPLETE (mistral-large2)
- Cortex Analyst + Semantic Views (linguagem natural para SQL)
- Cortex Search (pesquisa semantica em documentos)
- Cortex Agents (orquestracao multi-ferramenta)
- ML Functions: FORECAST, ANOMALY_DETECTION
- Streamlit in Snowflake e Native Apps

## Como Usar

### Pre-requisitos
- Conta Snowflake (trial ou existente)
- Role `ACCOUNTADMIN` (para setup inicial)
- Warehouse XS disponivel

### Opcao 1: Notebooks (Recomendado)
1. Fazer upload das notebooks para o Snowflake Workspace
2. Executar as celulas sequencialmente durante a demo

### Opcao 2: Scripts SQL
```sql
-- Executar os scripts pela ordem:
@00_setup_environment.sql
@01_data_loading.sql
@02_governance_demo.sql
@03_performance_cost.sql
@04_dynamic_tables.sql
@05_cortex_ai_demo.sql
@05b_cortex_agent_demo.sql
```

### Streamlit App
A app e deployada automaticamente via PUT + CREATE STREAMLIT no schema `PARTNERS_LISBON_DEMO.APPS`.

### Limpeza
```sql
@99_cleanup.sql
```

## Snowflake Objects Criados

| Tipo | Nome | Descricao |
|------|------|-----------|
| Database | `PARTNERS_LISBON_DEMO` | Base de dados principal |
| Schemas | `RAW`, `ANALYTICS`, `GOVERNANCE`, `APPS` | Separacao por camada |
| Warehouse | `PARTNERS_WH` (XS), `PARTNERS_WH_MEDIUM` (M) | Computacao para demos |
| Roles | `ANALYST_ROLE`, `ENGINEER_ROLE` | Demo de RBAC |
| Dynamic Tables | `CUSTOMER_360`, `SALES_BY_CATEGORY`, `TOP_PRODUCTS` | ETL declarativo |
| Semantic View | `SV_SALES_ANALYTICS` | Cortex Analyst |
| Cortex Search | `REVIEWS_SEARCH` | Pesquisa em reviews |
| Agent | `PARTNERS_SALES_AGENT` | Orquestracao Analyst + Search |
| Masking Policies | `MASK_EMAIL`, `MASK_PHONE` | Seguranca de dados |
| Streamlit | `PARTNER_ENABLEMENT_LISBOA` | App de slides interativos |

## Recursos

- [Documentacao Snowflake](https://docs.snowflake.com)
- [Quickstarts](https://quickstarts.snowflake.com)
- [Snowflake University](https://learn.snowflake.com)
- [Comunidade](https://community.snowflake.com)
- [Conta Trial](https://signup.snowflake.com)

---

*Snowflake AI Data Cloud — A plataforma que unifica dados, IA e aplicacoes.*

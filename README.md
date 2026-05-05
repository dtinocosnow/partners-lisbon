# Snowflake AI Data Cloud — Partner Enablement Lisboa

Materiais para a sessao presencial de capacitacao tecnica de Partners em Lisboa, Portugal.

## Visao Geral

| | |
|---|---|
| **Duracao** | 3 horas |
| **Local** | Lisboa, Portugal |
| **Audiencia** | Data Analysts, Data Engineers, Architects |
| **Idioma** | Portugues (apresentacao) / Ingles (demos e SQL) |

### Oradores

- **Pedro Jose** — Visao estrategica e contexto de mercado | [LinkedIn](https://www.linkedin.com/in/pjose/)
- **David Tinoco** — Deep dives tecnicos e laboratorio pratico | [LinkedIn](https://www.linkedin.com/in/dtinocoreyes/)
- **Frederic Arendt** — Conclusao e Go-To-Market | [LinkedIn](https://www.linkedin.com/in/farendt/)

## Estrutura do Repositorio

```
partners-lisbon/
├── 01_agenda/                  # Agenda e one-pager da sessao
├── 03_demo_scripts/            # Scripts SQL para demos ao vivo
│   ├── 00_setup_environment.sql    # Setup: DB, schemas, warehouses, roles
│   ├── 01_data_loading.sql         # Carga de dados (5 tabelas e-commerce)
│   ├── 01b_snowpipe_demo.sql       # Demo Snowpipe (ingestao continua)
│   ├── 02_governance_demo.sql      # Masking policies + Row access
│   ├── 03_performance_cost.sql     # Warehouse sizing, caching, resource monitors
│   ├── 04_dynamic_tables.sql       # Dynamic Tables (ETL declarativo)
│   ├── 05_cortex_ai_demo.sql       # Cortex AI: Sentiment, Translate, Semantic View, ML Forecast
│   ├── 05b_cortex_agent_demo.sql   # Cortex Agent (Analyst + Search combinados)
│   ├── 06_apps_marketplace.sql     # Secure views, cloning, tags, Streamlit
│   └── 99_cleanup.sql              # Limpeza completa do ambiente
├── 04_hands_on_lab/            # Guia do laboratorio pratico (5 passos)
├── 05_enablement/              # Roadmap de capacitacao 60 dias
└── 06_resources/               # Links e referencias uteis
```

## Agenda da Sessao

| Hora | Sessao | Orador |
|------|--------|--------|
| 10:00 | Boas-vindas e Objetivos | Pedro Jose |
| 10:10 | Visao Geral do Snowflake AI Data Cloud | Pedro Jose |
| 10:40 | Aprofundamento I: Fundamentos da Plataforma + Demo | David Tinoco |
| 11:15 | Intervalo | |
| 11:25 | Aprofundamento II: IA e Aplicacoes + Demo | David Tinoco |
| 11:55 | Laboratorio Pratico Guiado | David Tinoco |
| 12:25 | Pausa | |
| 12:30 | Conclusao e Percurso de Capacitacao | Frederic Arendt |

## Temas Abordados

### Aprofundamento I — Fundamentos
- Snowsight (tour pela interface)
- RBAC, Masking Policies, Row Access Policies
- Virtual Warehouses e elasticidade
- Camadas de cache e desempenho
- Snowpipe (ingestao continua)
- Dynamic Tables (ETL declarativo)

### Aprofundamento II — IA e Aplicacoes
- Cortex AI: SENTIMENT, TRANSLATE, SUMMARIZE, CLASSIFY, COMPLETE
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

### Setup do Ambiente
```sql
-- Executar os scripts pela ordem:
-- 1. Setup
@00_setup_environment.sql

-- 2. Dados
@01_data_loading.sql

-- 3. Demos (executar conforme a sessao avanca)
@02_governance_demo.sql
@03_performance_cost.sql
@04_dynamic_tables.sql
@05_cortex_ai_demo.sql
@05b_cortex_agent_demo.sql
```

### Limpeza
```sql
@99_cleanup.sql
```

## Snowflake Objects Criados

| Tipo | Nome | Descricao |
|------|------|-----------|
| Database | `PARTNERS_LISBON_DEMO` | Base de dados principal |
| Schemas | `RAW`, `ANALYTICS`, `GOVERNANCE` | Separacao por camada |
| Warehouse | `PARTNERS_WH` (XS) | Computacao para demos |
| Roles | `ANALYST_ROLE`, `ENGINEER_ROLE` | Demo de RBAC |
| Dynamic Tables | `CUSTOMER_360`, `SALES_BY_CATEGORY`, `TOP_PRODUCTS` | ETL declarativo |
| Semantic View | `SV_SALES_ANALYTICS` | Cortex Analyst |
| Cortex Search | `REVIEWS_SEARCH` | Pesquisa em reviews |
| Agent | `PARTNERS_SALES_AGENT` | Orquestracao Analyst + Search |
| Masking Policies | `MASK_EMAIL`, `MASK_PHONE` | Seguranca de dados |

## Recursos

- [Documentacao Snowflake](https://docs.snowflake.com)
- [Quickstarts](https://quickstarts.snowflake.com)
- [Snowflake University](https://learn.snowflake.com)
- [Comunidade](https://community.snowflake.com)
- [Conta Trial](https://signup.snowflake.com)

---

*Snowflake AI Data Cloud — A plataforma que unifica dados, IA e aplicacoes.*

# Snowflake AI Data Cloud — Partner Enablement Lisboa

Materiais para a sessao presencial de capacitacao tecnica de Partners em Lisboa, Portugal.

## Visao Geral

| | |
|---|---|
| **Duracao** | 3 horas (10:00 - 13:00) |
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
├── 01_agenda/                          # Agenda e one-pager da sessao
├── 03_demo_scripts/
│   ├── notebooks/                      # Notebooks para demos ao vivo (Snowflake Workspace)
│   │   ├── aprofundamento_I.ipynb          # Demo I: Setup, Data Loading, Snowpipe, Governance, Performance
│   │   └── aprofundamento_II.ipynb         # Demo II: Dynamic Tables, Cortex AI, Agent, Apps
│   ├── 00_setup_environment.sql        # Setup: DB, schemas, warehouses, roles
│   ├── 01_data_loading.sql             # Carga de dados (5 tabelas e-commerce)
│   ├── 01b_snowpipe_demo.sql           # Demo Snowpipe (ingestao continua)
│   ├── 02_governance_demo.sql          # Masking policies + Row access
│   ├── 03_performance_cost.sql         # Warehouse sizing, caching, resource monitors
│   ├── 04_dynamic_tables.sql           # Dynamic Tables (ETL declarativo)
│   ├── 05_cortex_ai_demo.sql           # Cortex AI: Sentiment, Translate, Semantic View
│   ├── 05b_cortex_agent_demo.sql       # Cortex Agent (Analyst + Search)
│   ├── 06_apps_marketplace.sql         # Secure views, cloning, tags
│   └── 99_cleanup.sql                  # Limpeza completa do ambiente
├── 04_hands_on_lab/                    # Laboratorio pratico SuperNova
│   ├── lab_guide_pt.md                     # Guia completo do lab (PT)
│   └── setup_bronze.sql                    # Script de setup da camada Bronze
├── 05_enablement/                      # Percurso de capacitacao pos-sessao
│   └── enablement_roadmap_pt.md            # Roadmap 30-60 dias
├── 06_resources/                       # Links e referencias uteis
│   └── links_and_references.md             # Documentacao, quickstarts, certificacoes
└── README.md
```

## Agenda da Sessao

| Hora | Sessao | Orador |
|------|--------|--------|
| 10:00 | Boas-vindas e Objetivos | Pedro Jose |
| 10:10 | Visao Geral do Snowflake AI Data Cloud | Pedro Jose |
| 10:40 | **Aprofundamento I:** Fundamentos + Demo ao vivo | David Tinoco |
| 11:15 | *Intervalo* | |
| 11:25 | **Aprofundamento II:** IA e Aplicacoes + Demo ao vivo | David Tinoco |
| 11:55 | **Laboratorio Pratico** (hands-on guiado) | David Tinoco |
| 12:25 | *Pausa* | |
| 12:30 | Conclusao e Percurso de Capacitacao | Frederic Arendt |

## Conteudo por Secao

### Aprofundamento I — Fundamentos (`aprofundamento_I.ipynb`)
- Arquitectura multi-cluster de dados partilhados
- RBAC, Masking Policies, Row Access Policies
- Virtual Warehouses e elasticidade
- Camadas de cache e desempenho
- Snowpipe (ingestao continua)
- Resource Monitors (controlo de custos)

### Aprofundamento II — IA e Aplicacoes (`aprofundamento_II.ipynb`)
- Dynamic Tables (ETL declarativo)
- Cortex AI: SENTIMENT, TRANSLATE, SUMMARIZE, CLASSIFY, COMPLETE
- Cortex Analyst + Semantic Views (linguagem natural para SQL)
- Cortex Search (pesquisa semantica em documentos)
- Cortex Agents (orquestracao multi-ferramenta)
- Secure Data Sharing, Zero-Copy Cloning, Marketplace

### Laboratorio Pratico — SuperNova (`04_hands_on_lab/`)
- Cenario: SuperNova Supermercados — cadeia portuguesa com 12 lojas
- 4 passos: Marketplace + Bronze → Silver/Gold (dbt) → Streamlit Dashboard → Cortex Agent
- Duracoes: ~30 minutos total

## Como Usar

### Notebooks (Recomendado para demos)
1. Fazer upload das notebooks (`.ipynb`) para o Snowflake Workspace
2. Executar as celulas sequencialmente — cada notebook inclui markdown educativo, SQL e visualizacoes Python

### Scripts SQL (Alternativa)
```sql
-- Executar pela ordem:
@00_setup_environment.sql
@01_data_loading.sql
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

## Pre-requisitos

- Conta Snowflake (trial em [signup.snowflake.com](https://signup.snowflake.com))
- Role `ACCOUNTADMIN` (para setup inicial)
- Browser atualizado (Chrome, Firefox ou Edge)

## Snowflake Objects Criados

| Tipo | Nome | Descricao |
|------|------|-----------|
| Database | `PARTNERS_LISBON_DEMO` | Base de dados da demo |
| Schemas | `RAW`, `ANALYTICS`, `GOVERNANCE` | Separacao por camada |
| Warehouses | `PARTNERS_WH` (XS), `PARTNERS_WH_MEDIUM` (M) | Computacao |
| Roles | `ANALYST_ROLE`, `ENGINEER_ROLE` | Demo de RBAC |
| Dynamic Tables | `CUSTOMER_360`, `SALES_BY_CATEGORY`, `TOP_PRODUCTS` | ETL declarativo |
| Semantic View | `SV_SALES_ANALYTICS` | Cortex Analyst |
| Cortex Search | `REVIEWS_SEARCH` | Pesquisa em reviews |
| Agent | `PARTNERS_SALES_AGENT` | Analyst + Search combinados |
| Masking Policies | `MASK_EMAIL`, `MASK_PHONE` | Seguranca de dados |

## Recursos

- [Documentacao Snowflake](https://docs.snowflake.com)
- [Quickstarts](https://quickstarts.snowflake.com)
- [Snowflake University](https://learn.snowflake.com)
- [Comunidade](https://community.snowflake.com)
- [Conta Trial](https://signup.snowflake.com)

---

*Snowflake AI Data Cloud — A plataforma que unifica dados, IA e aplicacoes.*

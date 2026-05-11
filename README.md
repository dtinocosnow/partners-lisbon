# Snowflake AI Data Cloud — Partner Enablement

Materials for in-person technical enablement sessions for Partners. Available in **Portuguese** and **English**.

## Repository Structure

```
partners-lisbon/
├── PT/                         # 🇵🇹 Portuguese version
│   ├── 01_agenda/
│   ├── 03_demo_scripts/
│   ├── 04_hands_on_lab/
│   ├── 05_enablement/
│   └── 06_resources/
├── EN/                         # 🇬🇧 English version
│   ├── 01_agenda/
│   ├── 03_demo_scripts/
│   ├── 04_hands_on_lab/
│   ├── 05_enablement/
│   └── 06_resources/
└── README.md
```

## Session Overview

| | |
|---|---|
| **Duration** | 3 hours |
| **Location** | Lisbon, Portugal |
| **Audience** | Data Analysts, Data Engineers, Architects |

### Speakers

- **Pedro Jose** — Strategic vision and market context | [LinkedIn](https://www.linkedin.com/in/pjose/)
- **David Tinoco** — Technical deep dives and hands-on lab | [LinkedIn](https://www.linkedin.com/in/dtinocoreyes/)
- **Frederic Arendt** — Wrap-up and Go-To-Market | [LinkedIn](https://www.linkedin.com/in/farendt/)

## Agenda

| Time | Session | Speaker |
|------|---------|---------|
| 10:00 | Welcome and Objectives | Pedro Jose |
| 10:10 | Snowflake AI Data Cloud Overview | Pedro Jose |
| 10:40 | Deep Dive I: Platform Fundamentals + Demo | David Tinoco |
| 11:15 | Break | |
| 11:25 | Deep Dive II: AI and Applications + Demo | David Tinoco |
| 11:55 | Guided Hands-On Lab | David Tinoco |
| 12:25 | Short Break | |
| 12:30 | Wrap-Up and Enablement Path | Frederic Arendt |

## Contents per Folder

| Folder | Description |
|--------|-------------|
| `01_agenda/` | Session agenda one-pager |
| `03_demo_scripts/` | SQL scripts + Jupyter notebooks for live demos |
| `04_hands_on_lab/` | Guided lab (SuperNova supermarket scenario) |
| `05_enablement/` | 60-day enablement roadmap |
| `06_resources/` | Links, references, certifications |

## Topics Covered

### Deep Dive I — Platform Fundamentals
- RBAC, Masking Policies, Row Access Policies
- Virtual Warehouses and elasticity
- Cache layers and performance
- Snowpipe (continuous ingestion)
- Dynamic Tables (declarative ETL)

### Deep Dive II — AI and Applications
- Cortex AI: SENTIMENT, TRANSLATE, SUMMARIZE, CLASSIFY, COMPLETE
- Cortex Analyst + Semantic Views
- Cortex Search (semantic search)
- Cortex Agents (multi-tool orchestration)
- ML Functions: FORECAST, ANOMALY_DETECTION
- Streamlit, Native Apps, Marketplace

## How to Use

Pick your language folder (`PT/` or `EN/`) and follow the demo scripts in order:

```sql
@00_setup_environment.sql
@01_data_loading.sql
@02_governance_demo.sql
@03_performance_cost.sql
@04_dynamic_tables.sql
@05_cortex_ai_demo.sql
@05b_cortex_agent_demo.sql
@99_cleanup.sql
```

Or use the Jupyter notebooks in `03_demo_scripts/notebooks/` for an interactive demo experience.

## Resources

- [Snowflake Docs](https://docs.snowflake.com) | [Quickstarts](https://quickstarts.snowflake.com) | [University](https://learn.snowflake.com) | [Trial](https://signup.snowflake.com)

---

*Snowflake AI Data Cloud — The platform that unifies data, AI, and applications.*

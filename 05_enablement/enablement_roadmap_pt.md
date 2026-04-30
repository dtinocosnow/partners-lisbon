# Percurso de Capacitacao Snowflake para Partners

> **Documento pos-sessao** | Partner Enablement Lisboa
> Utilize este guia para planear a vossa jornada de capacitacao nos proximos 60 dias.

---

## Visao Geral do Percurso

```
Semana 1-2          Semana 3-4          Mes 2
[Exploracao]   -->  [Certificacao]  --> [Implementacao]
  Conta trial         SnowPro Core       Primeiro POC
  Quickstarts         Labs avancados     Demo asset
  Documentacao        Especializacao     GTM conjunto
```

---

## Fase 1: Exploracao (Semana 1-2)

### Acoes Imediatas (esta semana)

- [ ] **Criar conta trial Snowflake** (se ainda nao tiverem)
  - URL: https://signup.snowflake.com
  - Edicao recomendada: Enterprise (30 dias gratis, $400 em creditos)

- [ ] **Completar o Quickstart "Zero to Snowflake"**
  - URL: https://quickstarts.snowflake.com/guide/getting_started_with_snowflake
  - Duracao: ~45 minutos
  - Cobre: Criar objetos, carregar dados, queries basicas

- [ ] **Explorar Snowflake University**
  - URL: https://learn.snowflake.com
  - Cursos recomendados para comecar:
    - "Hands-On Essentials: Data Warehousing"
    - "Hands-On Essentials: Data Engineering"
    - "Hands-On Essentials: Collaboration, Marketplace & Cost Estimation"

### Quickstarts Recomendados por Perfil

#### Data Analysts
| Quickstart | Duracao | URL |
|-----------|---------|-----|
| Getting Started with Snowsight | 30 min | https://quickstarts.snowflake.com |
| Tasty Bytes - Zero to Snowflake | 45 min | https://quickstarts.snowflake.com |
| Getting Started with Cortex Analyst | 30 min | https://quickstarts.snowflake.com |

#### Data Engineers
| Quickstart | Duracao | URL |
|-----------|---------|-----|
| Getting Started with Dynamic Tables | 30 min | https://quickstarts.snowflake.com |
| Getting Started with Snowpipe Streaming | 45 min | https://quickstarts.snowflake.com |
| Getting Started with dbt | 60 min | https://quickstarts.snowflake.com |

#### Architects
| Quickstart | Duracao | URL |
|-----------|---------|-----|
| Data Engineering with Snowpark Python | 60 min | https://quickstarts.snowflake.com |
| Getting Started with Iceberg Tables | 45 min | https://quickstarts.snowflake.com |
| Build a Native App | 60 min | https://quickstarts.snowflake.com |

---

## Fase 2: Certificacao (Semana 3-4)

### SnowPro Core Certification

A certificacao SnowPro Core e o ponto de partida recomendado para **todos os perfis**.

**Detalhes:**
- **Formato:** Exame online (65 questoes, 115 minutos)
- **Custo:** $175 USD
- **Preparacao:** 2-3 semanas de estudo
- **Validade:** 2 anos

**Topicos do exame:**
1. Snowflake Cloud Data Platform Features & Architecture
2. Account Access and Security
3. Performance Concepts
4. Data Loading and Unloading
5. Data Transformations
6. Data Protection and Data Sharing

**Recursos de preparacao:**
- Guia de estudo oficial: https://learn.snowflake.com/courses/uni-spcc-preparation
- Documentacao: https://docs.snowflake.com
- Pratica na conta trial

### Certificacoes Avancadas (apos Core)

| Certificacao | Perfil-alvo | Pre-requisito |
|-------------|-------------|---------------|
| SnowPro Advanced: Data Architect | Architects | SnowPro Core |
| SnowPro Advanced: Data Engineer | Data Engineers | SnowPro Core |
| SnowPro Advanced: Data Analyst | Analysts | SnowPro Core |
| SnowPro Advanced: Administrator | Admins/DBAs | SnowPro Core |

**Recomendacao:** Nomear 2-3 pessoas da equipa para completar SnowPro Core nas proximas 4 semanas.

---

## Fase 3: Implementacao (Mes 2)

### Desenvolver um Demo Asset Interno

Criar uma demonstracao que possam usar com os vossos clientes:

1. **Escolher um cenario** relevante para o vosso mercado
   - Exemplo: Retail analytics, Financial reporting, IoT data processing
2. **Implementar em Snowflake**
   - Base de dados + dados de amostra
   - 2-3 transformacoes (Dynamic Tables ou dbt)
   - 1 politica de governanca
   - 1 funcao Cortex AI
3. **Documentar e testar**

### Identificar Primeiro POC

- Selecionar 1-2 clientes com potencial para Snowflake
- Definir caso de uso especifico e mensuravel
- Alinhar com a equipa Snowflake para suporte tecnico

### Definir Plays Internas

Criar "plays" internas na vossa organizacao:
- **Play de Modernizacao de Data Warehouse** - Migracao de legacy para Snowflake
- **Play de Governance** - Implementar Horizon para clientes com requisitos de compliance
- **Play de IA** - Demonstrar Cortex AI para analise de dados e NLP
- **Play de Aplicacoes** - Construir aplicacoes Streamlit sobre dados em Snowflake

---

## Recursos Essenciais

### Documentacao e Aprendizagem

| Recurso | URL | Descricao |
|---------|-----|-----------|
| Documentacao Oficial | https://docs.snowflake.com | Referencia tecnica completa |
| Quickstart Guides | https://quickstarts.snowflake.com | Tutoriais praticos passo-a-passo |
| Snowflake University | https://learn.snowflake.com | Cursos e paths de certificacao |
| Community | https://community.snowflake.com | Forum da comunidade |
| GitHub Snowflake Labs | https://github.com/Snowflake-Labs | Exemplos de codigo e projetos |
| Medium Blog | https://medium.com/snowflake | Artigos tecnicos |

### Canais para Partners

| Recurso | URL | Descricao |
|---------|-----|-----------|
| Partner Portal | https://partners.snowflake.com | Portal de partners |
| Partner Courses | https://learn.snowflake.com/en/partners/ | Cursos especificos para partners |
| Brand Guidelines | https://www.snowflake.com/brand-guidelines | Templates e guias de marca |
| Conta Trial | https://signup.snowflake.com | Criar conta de trial gratuita |

### Ferramentas Complementares

| Ferramenta | Descricao |
|-----------|-----------|
| SnowCLI | CLI oficial para desenvolvimento local |
| VS Code Extension | Extensao para desenvolvimento SQL |
| dbt | Framework de transformacao de dados |
| Cortex Code (CoCo) | IDE integrada com IA para Snowflake |

---

## Checklist dos Proximos 60 Dias

### Semana 1
- [ ] Conta trial criada e funcional
- [ ] Quickstart "Zero to Snowflake" completado
- [ ] Snowflake University explorada

### Semana 2
- [ ] 2-3 quickstarts adicionais completados (por perfil)
- [ ] Documentacao de referencia revista

### Semana 3
- [ ] Inicio da preparacao para SnowPro Core
- [ ] 2-3 engenheiros nomeados para certificacao

### Semana 4
- [ ] Exame SnowPro Core agendado ou completado
- [ ] Primeiro caso de uso para POC identificado

### Mes 2
- [ ] Demo asset interno desenvolvido
- [ ] POC iniciado com pelo menos 1 cliente
- [ ] Play interna definida na organizacao
- [ ] Contas target para GTM conjunto identificadas
- [ ] Sessao de follow-up tecnico agendada com Snowflake

---

## Contactos

Para questoes tecnicas ou suporte no vosso percurso de capacitacao:

- **Pedro** - [email] - Estrategia e GTM
- **David** - [email] - Suporte tecnico e demos
- **Partner Team Iberia** - [email]

---

*Snowflake AI Data Cloud - A plataforma que unifica dados, IA e aplicacoes*

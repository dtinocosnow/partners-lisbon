import streamlit as st

st.markdown("""
<div style="border-left: 5px solid #FF9F36; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #11567F !important; margin: 0;">Laboratorio Pratico & Recursos</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">Hands-on &bull; Percurso de capacitacao &bull; Links uteis</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Lab Guide", "Percurso 30-60 dias", "Certificacoes", "Recursos"])

with tab1:
    st.markdown("### SuperNova Supermercados - Lab Pratico")
    st.caption("30 minutos | 1 SQL script + 3 prompts no Cortex Code")

    st.markdown("""
<div class="sf-card sf-card-accent">
<strong>Cenario:</strong> A SuperNova e uma cadeia de supermercados portuguesa com 12 lojas.
Vamos construir a plataforma de dados completa com dados REAIS do Marketplace
usando apenas <strong>1 script SQL e 3 prompts</strong> no Cortex Code.
</div>
""", unsafe_allow_html=True)

    st.markdown("#### Pre-requisitos")
    st.markdown("""
- Browser aberto em [app.snowflake.com](https://app.snowflake.com)
- Sessao iniciada na conta (trial ou demo)
- Role `ACCOUNTADMIN` selecionado
- Cortex Code aberto
""")

    st.markdown("---")
    st.markdown("#### Percurso do Laboratorio")

    steps = [
        ("Passo 1", "Marketplace + Bronze", "Obter dados ECB do Marketplace e carregar dados brutos", "5 min", "#29B5E8"),
        ("Passo 2", "Silver & Gold (dbt)", "Prompt que cria um dbt project com transformacoes", "8 min", "#11567F"),
        ("Passo 3", "Streamlit App", "Prompt que cria um dashboard executivo interativo", "8 min", "#7D44CF"),
        ("Passo 4", "Cortex Agent", "Prompt que cria um assistente inteligente de vendas", "9 min", "#FF9F36"),
    ]

    for step, title, desc, tempo, color in steps:
        st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 80px; font-weight: 700; color: {color};">{step}</div>
    <div style="flex: 1;"><strong>{title}</strong> &mdash; {desc}</div>
    <div style="background: #F0F4F8; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; color: #8A999E;">{tempo}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Os 3 Prompts")

    with st.expander("Prompt 1 - dbt Project (Silver + Gold)"):
        st.code("""Cria um dbt project chamado SUPERNOVA_TRANSFORMS para o supermercado SuperNova.
O projeto deve transformar os dados brutos da base SUPERNOVA_LAB.BRONZE em
tabelas analiticas organizadas em duas camadas:

Camada Silver: vendas enriquecidas + visao 360 do cliente
Camada Gold: KPIs diarios por loja, vendas por categoria, ranking de produtos

Faz deploy e executa para materializar todas as tabelas.""", language="text")

    with st.expander("Prompt 2 - Streamlit CEO Dashboard"):
        st.code("""Cria uma Streamlit app chamada SuperNova_CEO_Dashboard em SUPERNOVA_LAB.APPS
com painel estrategico para o CEO: 4 KPIs com deltas, filtros de periodo/loja/regiao,
grafico evolucao receita diaria, receita por loja, receita por categoria,
top 10 produtos e tabela de metricas por loja. Design profissional.
NAO usar hide_index, container(border=True) nem icones :material/.""", language="text")

    with st.expander("Prompt 3 - Cortex Agent"):
        st.code("""Cria um Cortex Agent chamado ANALISTA_SUPERNOVA em SUPERNOVA_LAB.GOLD
que responda perguntas sobre vendas e KPIs (dados Gold) e pesquise
avaliacoes de clientes (reviews Bronze). Responde em Portugues.
Cria Semantic View e Cortex Search Service necessarios.""", language="text")

    with st.expander("Perguntas de teste para o Agent"):
        st.markdown("""
- "Qual a loja com mais receita?"
- "O que dizem os clientes sobre o bacalhau?"
- "Top 5 produtos por vendas"
- "Mostra a receita por mes num grafico"
- "Quais produtos tem piores avaliacoes?"
""")

    st.markdown("---")
    st.markdown("#### Arquitetura Final")
    st.code("""SUPERNOVA_LAB
|-- BRONZE (dados brutos)
|   |-- Lojas, Produtos, Clientes
|   |-- Vendas (3000 transacoes)
|   |-- Reviews (20 avaliacoes PT)
|   +-- CPI_Alimentos_Portugal (Marketplace ECB)
|-- SILVER (dados enriquecidos) [dbt]
|   |-- Vendas_Enriquecidas
|   +-- Clientes_360
|-- GOLD (metricas negocio) [dbt]
|   |-- KPI_Diario
|   |-- Vendas_Categoria_Mensal
|   +-- Top_Produtos
+-- APPS / AI & ML
    |-- Streamlit Dashboard
    |-- Semantic View + Search Service
    +-- Cortex Agent (ANALISTA_SUPERNOVA)""", language="text")

with tab2:
    st.markdown("### Percurso de Capacitacao")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
<div class="sf-card" style="border-top: 3px solid #29B5E8;">
<h4 style="margin-top:0; color: #29B5E8 !important;">Semana 1-2</h4>
<ul>
<li>Criar conta trial e explorar</li>
<li>Completar quickstart "Zero to Snowflake"</li>
<li>Explorar Snowflake University</li>
<li>Familiarizar-se com Snowsight</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="sf-card" style="border-top: 3px solid #7D44CF;">
<h4 style="margin-top:0; color: #7D44CF !important;">Semana 3-4</h4>
<ul>
<li>Preparar SnowPro Core</li>
<li>Completar 2-3 quickstarts por perfil</li>
<li>Identificar caso de uso para POC</li>
<li>Explorar Cortex AI</li>
</ul>
</div>
""", unsafe_allow_html=True)

    with col3:
        st.markdown("""
<div class="sf-card" style="border-top: 3px solid #FF9F36;">
<h4 style="margin-top:0; color: #FF9F36 !important;">Mes 2</h4>
<ul>
<li>Certificacao SnowPro Core</li>
<li>Primeiro POC ou demo asset</li>
<li>Definir plays internas</li>
<li>Agendar sessao follow-up</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Acoes concretas")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Proximos 30 dias:**")
        st.markdown("""
- [ ] Completar quickstart "Zero to Snowflake"
- [ ] Nomear 2-3 engenheiros para certificacao
- [ ] Identificar primeiro caso de uso para POC
""")
    with col2:
        st.markdown("**Proximos 60 dias:**")
        st.markdown("""
- [ ] Desenvolver demo asset ou play interna
- [ ] Definir contas target para GTM conjunto
- [ ] Agendar sessao de follow-up tecnico
""")

with tab3:
    st.markdown("### Certificacoes SnowPro")

    st.dataframe(
        [
            {"Certificacao": "SnowPro Core", "Perfil": "Todos", "Nivel": "Fundamental", "Recomendacao": "Comecar aqui"},
            {"Certificacao": "Advanced Architect", "Perfil": "Architects", "Nivel": "Avancado", "Recomendacao": "Apos Core"},
            {"Certificacao": "Advanced Data Engineer", "Perfil": "Data Engineers", "Nivel": "Avancado", "Recomendacao": "Apos Core"},
            {"Certificacao": "Advanced Data Analyst", "Perfil": "Analysts", "Nivel": "Avancado", "Recomendacao": "Apos Core"},
            {"Certificacao": "Advanced Administrator", "Perfil": "Admins", "Nivel": "Avancado", "Recomendacao": "Apos Core"},
        ],
        use_container_width=True,
    )

    st.info("A certificacao **SnowPro Core** e o ponto de partida recomendado para todos. Disponivel em [learn.snowflake.com](https://learn.snowflake.com).")

with tab4:
    st.markdown("### Recursos Essenciais")

    resources = [
        ("Documentacao", "https://docs.snowflake.com"),
        ("Quickstarts", "https://quickstarts.snowflake.com"),
        ("University", "https://learn.snowflake.com"),
        ("Comunidade", "https://community.snowflake.com"),
        ("GitHub Labs", "https://github.com/Snowflake-Labs"),
        ("Conta Trial", "https://signup.snowflake.com"),
        ("Brand Guidelines", "https://www.snowflake.com/brand-guidelines"),
    ]

    for name, url in resources:
        st.markdown(f"""
<div style="display: flex; align-items: center; padding: 8px 12px; margin: 4px 0; border-left: 3px solid #29B5E8; background: #F8FBFF; border-radius: 0 6px 6px 0;">
<strong style="min-width: 140px; color: #11567F;">{name}</strong>
<a href="{url}" style="color: #29B5E8 !important;">{url}</a>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Contactos")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
<div class="sf-card" style="text-align: center;">
<strong>Pedro Jose</strong><br>
<span style="color: #8A999E; font-size: 0.85rem;">Visao estrategica</span><br>
<a href="https://www.linkedin.com/in/pjose/">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
<div class="sf-card" style="text-align: center;">
<strong>David Tinoco</strong><br>
<span style="color: #8A999E; font-size: 0.85rem;">Deep dives tecnicas</span><br>
<a href="https://www.linkedin.com/in/dtinocoreyes/">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
<div class="sf-card" style="text-align: center;">
<strong>Frederic Arendt</strong><br>
<span style="color: #8A999E; font-size: 0.85rem;">GTM & Partnerships</span><br>
<a href="https://www.linkedin.com/in/farendt/">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

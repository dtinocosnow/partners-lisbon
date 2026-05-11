import streamlit as st
from i18n import t

st.markdown(f"""
<div style="border-left: 5px solid #FF9F36; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #11567F !important; margin: 0;">{t('lab_title')}</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">{t('lab_sub')}</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(t("lab_tabs"))

with tab1:
    st.markdown(t("lab_scenario_title"))
    st.caption(t("lab_scenario_cap"))
    st.markdown(f'<div class="sf-card sf-card-accent">{t("lab_scenario_desc")}</div>', unsafe_allow_html=True)
    st.markdown(t("lab_prereqs_title"))
    st.markdown(t("lab_prereqs"))
    st.markdown("---")
    st.markdown(t("lab_path_title"))

    for step, title, desc, tempo, color in t("lab_steps"):
        st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 80px; font-weight: 700; color: {color};">{step}</div>
    <div style="flex: 1;"><strong>{title}</strong> &mdash; {desc}</div>
    <div style="background: #F0F4F8; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; color: #8A999E;">{tempo}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("lab_prompts_title"))

    with st.expander(t("lab_prompt1_title")):
        st.code("Cria um dbt project chamado SUPERNOVA_TRANSFORMS...\n(see lab_guide for full prompt)", language="text")
    with st.expander(t("lab_prompt2_title")):
        st.code("Cria uma Streamlit app chamada SuperNova_CEO_Dashboard...\n(see lab_guide for full prompt)", language="text")
    with st.expander(t("lab_prompt3_title")):
        st.code("Cria um Cortex Agent chamado ANALISTA_SUPERNOVA...\n(see lab_guide for full prompt)", language="text")
    with st.expander(t("lab_agent_questions_title")):
        st.markdown(t("lab_agent_questions"))

    st.markdown("---")
    st.markdown(t("lab_arch_title"))
    st.code("""SUPERNOVA_LAB
|-- BRONZE (raw data)
|   |-- Lojas, Produtos, Clientes
|   |-- Vendas (3000 transactions)
|   |-- Reviews (20 reviews PT)
|   +-- CPI_Alimentos_Portugal (Marketplace ECB)
|-- SILVER (enriched) [dbt]
|   |-- Vendas_Enriquecidas
|   +-- Clientes_360
|-- GOLD (business metrics) [dbt]
|   |-- KPI_Diario
|   |-- Vendas_Categoria_Mensal
|   +-- Top_Produtos
+-- APPS / AI & ML
    |-- Streamlit Dashboard
    |-- Semantic View + Search Service
    +-- Cortex Agent""", language="text")

with tab2:
    st.markdown(t("road_title"))
    c1, c2, c3 = st.columns(3)
    for col, title_key, items_key, color in [(c1, "road_w12_title", "road_w12", "#29B5E8"), (c2, "road_w34_title", "road_w34", "#7D44CF"), (c3, "road_m2_title", "road_m2", "#FF9F36")]:
        with col:
            li = "".join(f"<li>{x}</li>" for x in t(items_key))
            st.markdown(f'<div class="sf-card" style="border-top: 3px solid {color};"><h4 style="margin-top:0; color: {color} !important;">{t(title_key)}</h4><ul>{li}</ul></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(t("road_actions_title"))
    ca, cb = st.columns(2)
    with ca:
        st.markdown(t("road_30_title"))
        st.markdown(t("road_30"))
    with cb:
        st.markdown(t("road_60_title"))
        st.markdown(t("road_60"))

with tab3:
    st.markdown(t("cert_title"))
    st.dataframe(t("cert_data"), use_container_width=True)
    st.info(t("cert_info"))

with tab4:
    st.markdown(t("res_title"))
    resources = [
        ("Documentation", "https://docs.snowflake.com"),
        ("Quickstarts", "https://quickstarts.snowflake.com"),
        ("University", "https://learn.snowflake.com"),
        ("Community", "https://community.snowflake.com"),
        ("GitHub Labs", "https://github.com/Snowflake-Labs"),
        ("Trial Account", "https://signup.snowflake.com"),
        ("Brand Guidelines", "https://www.snowflake.com/brand-guidelines"),
    ]
    for name, url in resources:
        st.markdown(f'<div style="display: flex; align-items: center; padding: 8px 12px; margin: 4px 0; border-left: 3px solid #29B5E8; background: #F8FBFF; border-radius: 0 6px 6px 0;"><strong style="min-width: 140px; color: #11567F;">{name}</strong><a href="{url}" style="color: #29B5E8 !important;">{url}</a></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(t("contacts_title"))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="sf-card" style="text-align: center;"><strong>Pedro Jose</strong><br><span style="color: #8A999E; font-size: 0.85rem;">{t("pedro_role")}</span><br><a href="https://www.linkedin.com/in/pjose/">LinkedIn</a></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="sf-card" style="text-align: center;"><strong>David Tinoco</strong><br><span style="color: #8A999E; font-size: 0.85rem;">{t("david_role")}</span><br><a href="https://www.linkedin.com/in/dtinocoreyes/">LinkedIn</a></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sf-card" style="text-align: center;"><strong>Frederic Arendt</strong><br><span style="color: #8A999E; font-size: 0.85rem;">GTM & Partnerships</span><br><a href="https://www.linkedin.com/in/farendt/">LinkedIn</a></div>', unsafe_allow_html=True)

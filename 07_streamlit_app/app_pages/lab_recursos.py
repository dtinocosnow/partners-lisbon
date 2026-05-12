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
    st.markdown(t("trial_title"))
    st.markdown(f'<a href="{t("trial_url")}" target="_blank"><div style="background: linear-gradient(135deg, #11567F 0%, #29B5E8 100%); color: white; padding: 14px 24px; border-radius: 10px; text-align: center; font-weight: 700; font-size: 1.05rem; cursor: pointer; margin-bottom: 1rem; text-decoration: none;">&#x2744; {t("trial_btn")}</a></div>', unsafe_allow_html=True)

    for num, title, desc, color in t("trial_steps"):
        st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 32px; width: 32px; height: 32px; background: {color}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;">{num}</div>
    <div style="flex: 1; padding-left: 0.5rem;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.9rem;">{desc}</span></div>
</div>
""", unsafe_allow_html=True)

    st.info(t("trial_tip_cloud"))
    st.warning(t("trial_tip_edition"))

    st.markdown(t("trial_summary_title"))
    summary_html = ""
    for label, value in t("trial_summary"):
        summary_html += f'<div style="display:flex; justify-content:space-between; padding:8px 16px; border-bottom:1px solid #E8F4FA;"><span style="color:#8A999E; font-weight:600;">{label}</span><span style="color:#11567F; font-weight:700;">{value}</span></div>'
    st.markdown(f'<div class="sf-card" style="padding:0; overflow:hidden;">{summary_html}</div>', unsafe_allow_html=True)

    st.markdown("---")
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
    st.markdown(t("lab_step1_title"))
    st.markdown(t("lab_step1_intro"))

    with st.expander(t("lab_step1_terms_title"), expanded=False):
        for num, title, desc, color in t("lab_step1_terms_steps"):
            st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 32px; width: 32px; height: 32px; background: {color}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;">{num}</div>
    <div style="flex: 1; padding-left: 0.5rem;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.9rem;">{desc}</span></div>
</div>
""", unsafe_allow_html=True)
        st.info(t("lab_step1_terms_tip"))

    with st.expander(t("lab_step1_get_title"), expanded=True):
        st.markdown(f'<a href="{t("lab_step1_listing_url")}" target="_blank"><div style="background: linear-gradient(135deg, #11567F 0%, #29B5E8 100%); color: white; padding: 12px 20px; border-radius: 10px; text-align: center; font-weight: 700; font-size: 1rem; cursor: pointer; margin-bottom: 1rem; text-decoration: none;">&#x1F4E6; {t("lab_step1_get_btn")} &mdash; {t("lab_step1_listing_name")} ({t("lab_step1_listing_provider")})</div></a>', unsafe_allow_html=True)
        for num, title, desc, color in t("lab_step1_get_steps"):
            st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 32px; width: 32px; height: 32px; background: {color}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;">{num}</div>
    <div style="flex: 1; padding-left: 0.5rem;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.9rem;">{desc}</span></div>
</div>
""", unsafe_allow_html=True)
        st.success(t("lab_step1_get_tip"))
        st.warning(t("lab_step1_get_note"))

    with st.expander(t("lab_step1_verify_title"), expanded=False):
        st.markdown(t("lab_step1_verify_desc"))
        st.code(t("lab_step1_verify_sql"), language="sql")

    with st.expander(t("lab_step1_bronze_title"), expanded=True):
        for num, title, desc, color in t("lab_step1_bronze_steps"):
            st.markdown(f"""
<div class="sf-timeline-item" style="border-left: 4px solid {color};">
    <div style="min-width: 32px; width: 32px; height: 32px; background: {color}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;">{num}</div>
    <div style="flex: 1; padding-left: 0.5rem;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.9rem;">{desc}</span></div>
</div>
""", unsafe_allow_html=True)
        st.markdown(t("lab_step1_bronze_result"))
        result_html = ""
        for label, value in t("lab_step1_bronze_table"):
            result_html += f'<div style="display:flex; justify-content:space-between; padding:6px 16px; border-bottom:1px solid #E8F4FA;"><span style="color:#8A999E; font-weight:600;">{label}</span><span style="color:#11567F; font-weight:700;">{value}</span></div>'
        st.markdown(f'<div class="sf-card" style="padding:0; overflow:hidden;">{result_html}</div>', unsafe_allow_html=True)
        st.info(t("lab_step1_bronze_tip"))

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
    st.markdown(t("lab_nextsteps_title"))
    ns_cols = st.columns(4)
    for col, (step, desc, color) in zip(ns_cols, t("lab_nextsteps_steps")):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top:3px solid {color}; text-align:center; min-height:100px;"><div style="font-weight:800; color:{color}; font-size:1rem;">{step}</div><div style="color:#8A999E; font-size:0.85rem; margin-top:0.3rem;">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
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
    st.markdown(t("fy27_apps_title"))
    st.markdown(f'<p class="sf-big-text">{t("fy27_apps_desc")}</p>', unsafe_allow_html=True)
    ap1, ap2 = st.columns(2)
    with ap1:
        st.markdown(t("fy27_postgres_title"))
        st.markdown(t("fy27_postgres_desc"))
    with ap2:
        st.markdown(t("fy27_marketplace_title"))
        st.markdown(t("fy27_marketplace_desc"))

    st.markdown("---")
    st.markdown(t("fy27_finops_title"))
    st.markdown(t("fy27_finops_desc"))
    fo_cols = st.columns(3)
    fo_colors = ["#29B5E8", "#7D44CF", "#FF9F36"]
    for col, (title, desc), clr in zip(fo_cols, t("fy27_finops_pillars"), fo_colors):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top:3px solid {clr};"><strong style="color:{clr};">{title}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("fy27_sharing_title"))
    st.markdown(f'<div class="sf-card sf-card-accent">{t("fy27_sharing_desc")}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("lab_partners_title"))
    st.markdown(t("lab_partners_intro"))
    badges = "".join(f'<span style="background:#EBF7FD; color:#11567F; padding:6px 14px; border-radius:20px; font-weight:600; font-size:0.85rem;">{p}</span>' for p in t("lab_partners_list"))
    st.markdown(f'<div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin:0.5rem 0;">{badges}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("lab_integrations_title"))
    st.markdown(t("lab_integrations_intro"))
    ig_cols = st.columns(3)
    ig_colors = ["#29B5E8", "#7D44CF", "#FF9F36"]
    for col, (name, desc), clr in zip(ig_cols, t("lab_integrations_items"), ig_colors):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top:3px solid {clr};"><strong style="color:{clr};">{name}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("lab_unified_title"))
    st.success(t("lab_unified_desc"))

    st.markdown("---")
    st.markdown(t("contacts_title"))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="sf-card" style="text-align: center;"><strong>Pedro Jose</strong><br><span style="color: #8A999E; font-size: 0.85rem;">{t("pedro_role")}</span><br><a href="https://www.linkedin.com/in/pjose/">LinkedIn</a></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="sf-card" style="text-align: center;"><strong>David Tinoco</strong><br><span style="color: #8A999E; font-size: 0.85rem;">{t("david_role")}</span><br><a href="https://www.linkedin.com/in/dtinocoreyes/">LinkedIn</a></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="sf-card" style="text-align: center;"><strong>Frederic Arendt</strong><br><span style="color: #8A999E; font-size: 0.85rem;">GTM & Partnerships</span><br><a href="https://www.linkedin.com/in/farendt/">LinkedIn</a></div>', unsafe_allow_html=True)

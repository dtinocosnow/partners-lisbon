import streamlit as st
from i18n import t

st.markdown(f"""
<div style="border-left: 5px solid #7D44CF; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #7D44CF !important; margin: 0;">{t('dd2_title')}</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">{t('dd2_sub')}</p>
</div>
""", unsafe_allow_html=True)

tab_cortex, tab_llm, tab_analyst, tab_search, tab_agents, tab_ml, tab_apps, tab_quiz = st.tabs(
    ["Cortex AI", "LLM Functions", "Analyst", "Search", "Agents", "ML & Migration", "Apps", "Quiz"]
)

with tab_cortex:
    st.markdown(t("dd2_cortex_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_cortex_intro")}</p>', unsafe_allow_html=True)

    cols = st.columns(5)
    for col, (title, desc, color) in zip(cols, t("dd2_cortex_caps")):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top: 3px solid {color}; text-align: center; min-height: 130px;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.85rem;">{desc}</span></div>', unsafe_allow_html=True)
    st.success(t("dd2_cortex_key"))

    st.markdown("---")
    st.markdown(t("fy27_cortex_stack_title"))
    fs_cols = st.columns(5)
    for col, (title, desc, color) in zip(fs_cols, t("fy27_cortex_stack_items")):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top: 3px solid {color}; min-height: 140px;"><strong style="color: {color};">{title}</strong><br><span style="color: #8A999E; font-size: 0.8rem;">{desc}</span></div>', unsafe_allow_html=True)

with tab_llm:
    st.markdown(t("dd2_llm_title"))
    st.markdown(t("dd2_llm_intro"))
    llm1, llm2, llm3, llm4, llm5 = st.tabs(["Sentiment", "Translate", "Summarize", "Classify", "Extract"])

    with llm1:
        st.code("SELECT review_text,\n       SNOWFLAKE.CORTEX.SENTIMENT(review_text) as score\nFROM product_reviews;\n-- score: -1.0 (negative) to 1.0 (positive)", language="sql")
    with llm2:
        st.code("SELECT SNOWFLAKE.CORTEX.TRANSLATE(\n  'Hello, how are you?', 'en', 'pt'\n);\n-- Result: 'Ola, como esta?'", language="sql")
    with llm3:
        st.code("SELECT SNOWFLAKE.CORTEX.SUMMARIZE(\n  document_text\n) as summary\nFROM contracts;", language="sql")
    with llm4:
        st.code("SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(\n  'The product arrived damaged and late',\n  ['positive', 'negative', 'neutral']\n);\n-- Result: 'negative'", language="sql")
    with llm5:
        st.code("SELECT SNOWFLAKE.CORTEX.EXTRACT(\n  document_text,\n  ['customer_name', 'total_value', 'invoice_date']\n) FROM invoices;", language="sql")

with tab_analyst:
    st.markdown(t("dd2_analyst_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_analyst_intro")}</p>', unsafe_allow_html=True)
    st.markdown(t("dd2_analyst_flow_title"))
    for num, desc in t("dd2_analyst_steps"):
        st.markdown(f'<div style="display: flex; align-items: center; margin: 4px 0;"><span style="background: #29B5E8; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 12px; flex-shrink: 0;">{num}</span><span style="font-size: 1rem;">{desc}</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(t("dd2_analyst_comp_title"))
        st.markdown(t("dd2_analyst_comp"))
    with c2:
        st.markdown(t("dd2_analyst_example"))
        st.code("CREATE SEMANTIC VIEW sv_sales_analytics\n  COMMENT = 'Sales analytics model'\n  TABLES (\n    o AS DB.SCHEMA.ORDERS\n      PRIMARY KEY (ORDER_ID)\n  )\n  METRICS (\n    total_revenue AS SUM(o.TOTAL_AMOUNT)\n      COMMENT 'Total sales revenue'\n  )\n  DIMENSIONS (\n    order_date AS o.ORDER_DATE\n      COMMENT 'Date of the order'\n  );", language="sql")

    st.markdown("---")
    st.markdown(t("dd2_semantic_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_semantic_intro")}</p>', unsafe_allow_html=True)
    sem1, sem2 = st.columns(2)
    with sem1:
        st.markdown(f'<div class="sf-card" style="border-top:3px solid #27AE60; text-align:center;"><div style="font-weight:700; color:#27AE60;">{t("dd2_semantic_with")}</div><div style="font-size:2rem; font-weight:800; color:#27AE60;">~100%</div></div>', unsafe_allow_html=True)
    with sem2:
        st.markdown(f'<div class="sf-card" style="border-top:3px solid #E74C3C; text-align:center;"><div style="font-weight:700; color:#E74C3C;">{t("dd2_semantic_without")}</div><div style="font-size:2rem; font-weight:800; color:#E74C3C;">&lt;50%</div></div>', unsafe_allow_html=True)
    st.info(t("dd2_semantic_accuracy"))

    st.markdown(t("dd2_semantic_benefits_title"))
    bc1, bc2, bc3 = st.columns(3)
    for col, (title, desc) in zip([bc1, bc2, bc3], t("dd2_semantic_benefits")):
        with col:
            st.markdown(f'<div class="sf-card"><strong style="color:#11567F;">{title}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sf-card sf-card-accent" style="text-align:center;"><div style="font-size:2.5rem; font-weight:800; color:#29B5E8;">{t("dd2_semantic_stat_val")}</div><div style="font-weight:600; color:#11567F;">{t("dd2_semantic_stat_label")}</div><div style="color:#8A999E; font-size:0.85rem;">{t("dd2_semantic_stat_detail")}</div></div>', unsafe_allow_html=True)

with tab_search:
    st.markdown(t("dd2_search_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_search_intro")}</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(t("dd2_search_how_title"))
        st.markdown(t("dd2_search_how"))
    with c2:
        st.markdown(t("dd2_search_cases_title"))
        st.markdown(t("dd2_search_cases"))
    st.code("CREATE CORTEX SEARCH SERVICE reviews_search\n  ON review_text\n  ATTRIBUTES product_name, rating\n  WAREHOUSE = partners_wh\n  TARGET_LAG = '1 hour'\nAS (\n  SELECT review_text, product_name, rating\n  FROM product_reviews\n);", language="sql")

with tab_agents:
    st.markdown(t("dd2_agents_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_agents_intro")}</p>', unsafe_allow_html=True)
    st.markdown(t("dd2_agents_example"))
    st.code("""CREATE OR REPLACE AGENT sales_assistant
FROM SPECIFICATION $$
models:
  orchestration: auto
instructions:
  system: "You are a sales analytics assistant."
  orchestration: "Use Analyst for revenue questions; Search for reviews."
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "sales_analyst"
      description: "Queries structured sales data"
  - tool_spec:
      type: "cortex_search"
      name: "reviews_search"
      description: "Searches customer reviews"
tool_resources:
  sales_analyst:
    semantic_view: "DB.SCHEMA.SV_SALES_ANALYTICS"
  reviews_search:
    name: "DB.SCHEMA.REVIEWS_SEARCH"
    max_results: "5"
$$;""", language="sql")
    st.markdown(t("dd2_agents_tools_title"))
    st.markdown(t("dd2_agents_tools"))

    st.markdown("---")
    ag1, ag2 = st.columns(2)
    with ag1:
        st.markdown(t("fy27_intelligence_title"))
        st.markdown(t("fy27_intelligence_desc"))
    with ag2:
        st.markdown(t("fy27_cortex_code_title"))
        st.markdown(t("fy27_cortex_code_desc"))

with tab_ml:
    st.markdown(t("dd2_ml_title"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(t("dd2_ml_forecast"))
        st.code("CREATE SNOWFLAKE.ML.FORECAST sales_forecast (\n  INPUT_DATA => TABLE(training_view),\n  TIMESTAMP_COLNAME => 'ORDER_DATE',\n  TARGET_COLNAME => 'DAILY_REVENUE'\n);\n\nCALL sales_forecast!FORECAST(30);", language="sql")
    with c2:
        st.markdown(t("dd2_ml_anomaly"))
        st.code("CREATE SNOWFLAKE.ML.ANOMALY_DETECTION detector (\n  INPUT_DATA => TABLE(training_data),\n  TIMESTAMP_COLNAME => 'DATA',\n  TARGET_COLNAME => 'VALOR'\n);\n\nCALL detector!DETECT_ANOMALIES(\n  INPUT_DATA => TABLE(new_data)\n);", language="sql")
    st.info(t("dd2_ml_info"))

    st.markdown("---")
    ml1, ml2 = st.columns(2)
    with ml1:
        st.markdown(t("fy27_ml_detail_title"))
        st.markdown(t("fy27_ml_detail_desc"))
        st.info(t("fy27_ml_case"))
    with ml2:
        st.markdown(t("fy27_trust_title"))
        st.markdown(t("fy27_trust_desc"))
        st.markdown(t("fy27_semantic_autopilot_title"))
        st.markdown(t("fy27_semantic_autopilot_desc"))

    st.markdown("---")
    st.markdown(t("dd2_snowconvert_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_snowconvert_intro")}</p>', unsafe_allow_html=True)
    sc_cols = st.columns(4)
    sc_colors = ["#29B5E8", "#7D44CF", "#FF9F36", "#71D3DC"]
    for col, (val, label), clr in zip(sc_cols, t("dd2_snowconvert_stats"), sc_colors):
        with col:
            st.markdown(f'<div class="sf-card" style="text-align:center; border-top:3px solid {clr};"><div style="font-size:1.5rem; font-weight:800; color:{clr};">{val}</div><div style="color:#8A999E; font-size:0.8rem;">{label}</div></div>', unsafe_allow_html=True)
    st.caption(t("dd2_snowconvert_sources"))

    st.markdown("---")
    st.markdown(t("dd2_applied_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_applied_intro")}</p>', unsafe_allow_html=True)
    ap_cols = st.columns(4)
    ap_colors = ["#29B5E8", "#11567F", "#7D44CF", "#FF9F36"]
    for col, (title, desc), clr in zip(ap_cols, t("dd2_applied_items"), ap_colors):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top:3px solid {clr}; min-height:100px;"><strong style="color:{clr};">{title}</strong><br><span style="color:#8A999E; font-size:0.8rem;">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(t("dd2_interactive_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd2_interactive_intro")}</p>', unsafe_allow_html=True)
    it_cols = st.columns(3)
    it_colors = ["#29B5E8", "#7D44CF", "#FF9F36"]
    for col, (title, desc), clr in zip(it_cols, t("dd2_interactive_cases"), it_colors):
        with col:
            st.markdown(f'<div class="sf-card" style="border-top:3px solid {clr};"><strong style="color:{clr};">{title}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)

with tab_apps:
    st.markdown(t("dd2_apps_title"))
    apps1, apps2 = st.tabs(["Streamlit in Snowflake", "Native Apps & Marketplace"])
    with apps1:
        st.markdown(f'<p class="sf-big-text">{t("dd2_streamlit_intro")}</p>', unsafe_allow_html=True)
        st.code('import streamlit as st\nfrom snowflake.snowpark.context import get_active_session\n\nsession = get_active_session()\nst.title("Sales Dashboard")\n\ndf = session.sql("SELECT * FROM analytics.monthly_sales").to_pandas()\nst.bar_chart(df, x="MONTH", y="TOTAL_SALES")', language="python")
        st.markdown(t("dd2_streamlit_benefits"))
    with apps2:
        st.markdown(f'<p class="sf-big-text">{t("dd2_native_intro")}</p>', unsafe_allow_html=True)
        st.markdown(t("dd2_native_flow"))
        st.success(t("dd2_native_gtm"))

with tab_quiz:
    st.markdown(t("dd2_quiz_title"))
    st.markdown(t("dd2_quiz_sub"))
    st.markdown("---")
    for i, (qkey, opts_key, ok_key, fail_key) in enumerate([
        ("dd2_q1", "dd2_q1_opts", "dd2_q1_ok", "dd2_q1_fail"),
        ("dd2_q2", "dd2_q2_opts", "dd2_q2_ok", "dd2_q2_fail"),
        ("dd2_q3", "dd2_q3_opts", "dd2_q3_ok", "dd2_q3_fail"),
    ], 1):
        st.markdown(f"#### {'Pergunta' if st.session_state.get('lang') == 'PT' else 'Question'} {i}")
        st.markdown(t(qkey))
        q = st.selectbox(t("select_label"), t(opts_key), index=0, key=f"q{i}_dd2")
        if q:
            correct = "B)" if i <= 2 else "C)"
            if i == 3:
                correct = "C)"
            if correct in q:
                st.success(t(ok_key))
            else:
                st.error(t(fail_key))
        st.markdown("---")

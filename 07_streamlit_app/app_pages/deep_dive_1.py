import streamlit as st
from i18n import t

st.markdown(f"""
<div style="border-left: 5px solid #11567F; padding-left: 1.2rem; margin-bottom: 1.5rem;">
    <h1 style="color: #11567F !important; margin: 0;">{t('dd1_title')}</h1>
    <p style="color: #8A999E; margin: 0.3rem 0 0 0; font-size: 1.05rem;">{t('dd1_sub')}</p>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(t("dd1_tabs"))

with tabs[0]:
    st.markdown(t("dd1_arch_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd1_arch_intro")}</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for col, key, color in [(col1, "dd1_cloud_svc", "#29B5E8"), (col2, "dd1_compute", "#7D44CF"), (col3, "dd1_storage", "#FF9F36")]:
        items_key = key.replace("dd1_", "dd1_") + "_items"
        items = t(items_key)
        with col:
            li = "".join(f"<li>{x}</li>" for x in items)
            st.markdown(f'<div class="sf-card sf-card-accent" style="border-left-color: {color};"><h4 style="margin-top:0;">{t(key)}</h4><ul>{li}</ul></div>', unsafe_allow_html=True)

    st.info(t("dd1_key_concept"))

    with st.expander(t("dd1_clone_title")):
        st.markdown(t("dd1_clone_desc"))
        st.code("CREATE DATABASE dev_environment CLONE production;\n-- Instant, no additional storage cost (until changes are made)", language="sql")
        st.markdown(t("dd1_clone_cases"))

    with st.expander(t("dd1_sharing_title")):
        st.markdown(t("dd1_sharing_desc"))

    with st.expander(t("dd1_multicloud_title")):
        st.markdown(t("dd1_multicloud_desc"))

with tabs[1]:
    st.markdown(t("dd1_sec_title"))
    seg_tabs = st.tabs(t("dd1_sec_tabs"))

    with seg_tabs[0]:
        st.markdown(t("dd1_rbac_title"))
        st.code("""ACCOUNTADMIN
  +-- SYSADMIN
  |    +-- DB_ADMIN
  |    |    +-- ANALYST_ROLE
  |    |    +-- ENGINEER_ROLE
  |    +-- CUSTOM_ROLES...
  +-- SECURITYADMIN""", language="text")
        st.dataframe(t("dd1_rbac_roles"), use_container_width=True)
        st.markdown(t("dd1_rbac_principles"))

    with seg_tabs[1]:
        st.markdown(t("dd1_mask_title"))
        st.markdown(t("dd1_mask_desc"))
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(t("dd1_mask_admin"))
            st.dataframe([{"EMAIL": "joao@empresa.pt", "TELEFONE": "+351 912 345 678"}], use_container_width=True)
        with c2:
            st.markdown(t("dd1_mask_analyst"))
            st.dataframe([{"EMAIL": "j***@***.pt", "TELEFONE": "***-***-678"}], use_container_width=True)
        st.code("""CREATE MASKING POLICY mask_email AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ADMIN') THEN val
    ELSE REGEXP_REPLACE(val, '.+@', '***@')
  END;

ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY mask_email;""", language="sql")

    with seg_tabs[2]:
        st.markdown(t("dd1_row_title"))
        st.markdown(t("dd1_row_desc"))
        st.code("""CREATE ROW ACCESS POLICY region_policy AS (region STRING)
  RETURNS BOOLEAN ->
  CURRENT_ROLE() = 'GLOBAL_ANALYST'
  OR region = 'EMEA';

ALTER TABLE orders ADD ROW ACCESS POLICY region_policy ON (region);""", language="sql")

    with seg_tabs[3]:
        st.markdown(t("dd1_horizon_title"))
        cols = st.columns(5)
        for col, (title, desc) in zip(cols, t("dd1_horizon_items")):
            with col:
                st.markdown(f'<div class="sf-card" style="text-align:center; padding: 1rem;"><strong>{title}</strong><br><span style="color:#8A999E; font-size:0.85rem;">{desc}</span></div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown(t("dd1_perf_title"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(t("dd1_wh_title"))
        st.dataframe(t("dd1_wh_data"), use_container_width=True)
    with c2:
        st.markdown(t("dd1_cache_title"))
        st.markdown(t("dd1_cache_html"), unsafe_allow_html=True)
        st.info(t("dd1_cache_tip"))
    st.markdown(t("dd1_best_title"))
    ca, cb = st.columns(2)
    with ca:
        st.markdown(t("dd1_best_l"))
    with cb:
        st.markdown(t("dd1_best_r"))

with tabs[3]:
    st.markdown(t("dd1_ing_title"))
    st.dataframe(t("dd1_ing_data"), use_container_width=True)
    with st.expander(t("dd1_ing_example")):
        st.code("""CREATE STAGE my_s3_stage URL = 's3://my-bucket/data/'
  CREDENTIALS = (AWS_KEY_ID='...' AWS_SECRET_KEY='...');

CREATE PIPE my_pipe AUTO_INGEST = TRUE AS
  COPY INTO raw.events FROM @my_s3_stage
  FILE_FORMAT = (TYPE = 'JSON');

SELECT SYSTEM$PIPE_STATUS('my_pipe');""", language="sql")

with tabs[4]:
    st.markdown(t("dd1_dt_title"))
    st.markdown(f'<p class="sf-big-text">{t("dd1_dt_intro")}</p>', unsafe_allow_html=True)
    st.code("""CREATE DYNAMIC TABLE analytics_orders
  TARGET_LAG = '1 hour'
  WAREHOUSE = wh_etl
AS
  SELECT
    o.order_date,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) as total_amount
  FROM raw.orders o
  JOIN raw.customers c ON o.customer_id = c.customer_id
  JOIN raw.order_items oi ON o.order_id = oi.order_id
  GROUP BY 1, 2;""", language="sql")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(t("dd1_dt_m1"), "Zero")
    with c2:
        st.metric(t("dd1_dt_m2"), "Incremental")
    with c3:
        st.metric(t("dd1_dt_m3"), "Lower" if st.session_state.get("lang") == "EN" else "Menor")
    st.markdown(t("dd1_dt_advantages"))

with tabs[5]:
    st.markdown(t("dd1_quiz_title"))
    st.markdown(t("dd1_quiz_sub"))
    st.markdown("---")

    for i, (qkey, opts_key, ok_key, fail_key) in enumerate([
        ("dd1_q1", "dd1_q1_opts", "dd1_q1_ok", "dd1_q1_fail"),
        ("dd1_q2", "dd1_q2_opts", "dd1_q2_ok", "dd1_q2_fail"),
        ("dd1_q3", "dd1_q3_opts", "dd1_q3_ok", "dd1_q3_fail"),
    ], 1):
        st.markdown(f"#### {'Pergunta' if st.session_state.get('lang') == 'PT' else 'Question'} {i}")
        st.markdown(t(qkey))
        q = st.selectbox(t("select_label"), t(opts_key), index=0, key=f"q{i}_dd1")
        if q:
            correct_letter = "B)" if i <= 2 else "C)"
            if i == 3:
                correct_letter = "C)"
            if correct_letter in q:
                st.success(t(ok_key))
            else:
                st.error(t(fail_key))
        st.markdown("---")

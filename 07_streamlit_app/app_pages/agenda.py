import streamlit as st
from i18n import t

st.markdown(f"""
<div class="sf-hero-banner">
    <h2>{t('hero_title')}</h2>
    <p>{t('hero_sub')}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<p class="sf-big-text">{t("objective")}</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(t("agenda_title"))

for time_slot, duration, session, speaker, color in t("agenda_items"):
    is_break = speaker == "---"
    bg = "#FAFAFA" if is_break else "#F8FBFF"
    st.markdown(f"""
    <div class="sf-timeline-item" style="border-left: 5px solid {color}; background: {bg};">
        <div style="min-width: 120px; color: {color}; font-weight: 700; font-size: 0.95rem;">{time_slot}</div>
        <div style="min-width: 65px; color: #8A999E; font-size: 0.8rem; background: #F0F4F8; padding: 2px 8px; border-radius: 12px;">{duration}</div>
        <div style="flex: 1; font-weight: 600; color: #24323D; padding-left: 1rem; font-size: 1.05rem;">{session}</div>
        <div style="color: #8A999E; font-size: 0.85rem; font-style: italic;">{speaker}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown(t("fy27_global_title"))
gc1, gc2, gc3 = st.columns(3)
for col, vk, lk, color in [(gc1, "fy27_global_customers", "fy27_global_customers_label", "#29B5E8"), (gc2, "fy27_global_ai", "fy27_global_ai_label", "#7D44CF"), (gc3, "fy27_global_fortune", "fy27_global_fortune_label", "#11567F")]:
    with col:
        st.markdown(f'<div class="sf-card" style="text-align:center; border-top: 3px solid {color};"><div style="font-size: 2rem; font-weight: 800; color: {color};">{t(vk)}</div><div style="color: #8A999E; font-size: 0.85rem; margin-top: 0.3rem;">{t(lk)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(t("fy27_easy_title"))
ec1, ec2, ec3 = st.columns(3)
for col, nk, dk, color in [(ec1, "fy27_easy", "fy27_easy_desc", "#29B5E8"), (ec2, "fy27_connected", "fy27_connected_desc", "#7D44CF"), (ec3, "fy27_trusted", "fy27_trusted_desc", "#FF9F36")]:
    with col:
        st.markdown(f'<div class="sf-card" style="border-top: 3px solid {color}; text-align:center; min-height:120px;"><div style="font-weight:800; color:{color}; font-size:1.1rem;">{t(nk)}</div><div style="color:#8A999E; font-size:0.85rem; margin-top:0.5rem;">{t(dk)}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(t("mod_why_title"))
mc1, mc2, mc3 = st.columns(3)
for col, vk, lk, color in [(mc1, "mod_stat1_val", "mod_stat1_label", "#E74C3C"), (mc2, "mod_stat2_val", "mod_stat2_label", "#FF9F36"), (mc3, "mod_stat3_val", "mod_stat3_label", "#7D44CF")]:
    with col:
        st.markdown(f'<div class="sf-card" style="text-align:center; border-top: 3px solid {color};"><div style="font-size: 2rem; font-weight: 800; color: {color};">{t(vk)}</div><div style="color: #8A999E; font-size: 0.85rem; margin-top: 0.3rem;">{t(lk)}</div></div>', unsafe_allow_html=True)

with st.expander(t("mod_imagine_title").replace("### ", "")):
    for item in t("mod_imagine_items"):
        st.markdown(f"- {item}")

with st.expander(t("mod_readiness_title").replace("### ", "")):
    for i, q in enumerate(t("mod_readiness_items"), 1):
        st.markdown(f"**{i}.** {q}")

with st.expander(t("mod_legacy_title").replace("### ", "")):
    headers = t("mod_legacy_headers")
    rows = t("mod_legacy_rows")
    header_html = "".join(f"<th style='padding:8px 12px; background:#11567F; color:white;'>{h}</th>" for h in headers)
    rows_html = ""
    for dim, legacy, modern in rows:
        rows_html += f"<tr><td style='padding:8px 12px; font-weight:600;'>{dim}</td><td style='padding:8px 12px; color:#E74C3C;'>{legacy}</td><td style='padding:8px 12px; color:#27AE60;'>{modern}</td></tr>"
    st.markdown(f"<table style='width:100%; border-collapse:collapse; font-size:0.9rem;'><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>", unsafe_allow_html=True)

st.markdown(t("mod_pillars_title"))
pc1, pc2, pc3 = st.columns(3)
for col, name_k, change_k, impact_k, color in [
    (pc1, "mod_pillar_speed", "mod_pillar_speed_change", "mod_pillar_speed_impact", "#29B5E8"),
    (pc2, "mod_pillar_cost", "mod_pillar_cost_change", "mod_pillar_cost_impact", "#FF9F36"),
    (pc3, "mod_pillar_trust", "mod_pillar_trust_change", "mod_pillar_trust_impact", "#7D44CF"),
]:
    with col:
        st.markdown(f'<div class="sf-card" style="border-top: 3px solid {color}; text-align:center;"><div style="font-weight:800; color:{color}; font-size:1.1rem;">{t(name_k)}</div><div style="color:#24323D; font-size:0.9rem; margin:0.5rem 0;">{t(change_k)}</div><div style="color:#8A999E; font-size:0.8rem;">{t(impact_k)}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(t("takeaways_title"))

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3, col1, col2, col3]

for i, (title, desc, color) in enumerate(t("takeaways")):
    with cols[i]:
        st.markdown(f"""
        <div class="sf-takeaway-card" style="border-top: 3px solid {color};">
            <div style="font-weight: 700; color: #11567F; font-size: 1rem; margin-bottom: 0.4rem;">{title}</div>
            <div style="color: #8A999E; font-size: 0.85rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(t("audience_title"))
    st.markdown("""
<div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Data Analysts</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Data Engineers</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Architects</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Tech Leaders</span>
</div>
""", unsafe_allow_html=True)

with col_b:
    st.markdown(t("prereqs_title"))
    st.markdown(t("prereqs_text"))

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

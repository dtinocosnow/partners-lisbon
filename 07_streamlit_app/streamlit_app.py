import streamlit as st
from i18n import t

st.set_page_config(layout="wide")

if "lang" not in st.session_state:
    st.session_state.lang = "PT"

def _sync_lang():
    st.session_state.lang = st.session_state._lang_radio

BRAND_CSS = """
<style>
:root {
    --sf-blue: #29B5E8;
    --sf-mid-blue: #11567F;
    --sf-midnight: #000000;
    --sf-star-blue: #71D3DC;
    --sf-orange: #FF9F36;
    --sf-purple: #7D44CF;
    --sf-rose: #D45B90;
    --sf-neutral: #8A999E;
    --sf-iceberg: #003545;
    --sf-winter: #24323D;
}

html { scroll-behavior: smooth; }

html, body, p, li, div, input, textarea, button, a, label, td, th {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    font-weight: 800 !important;
    color: var(--sf-mid-blue) !important;
}

h1 { letter-spacing: -0.5px !important; font-size: 2.2rem !important; }
h2 { font-size: 1.6rem !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8FBFF 0%, #EBF7FD 100%) !important;
    border-right: 2px solid #E8F4FA !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: radial-gradient(circle, #29B5E8 0.5px, transparent 0.5px);
    background-size: 20px 20px;
    opacity: 0.04;
    pointer-events: none;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: var(--sf-mid-blue) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

div[data-testid="stMetric"] {
    background-color: #F8FBFF;
    border: 1px solid #E8F4FA;
    border-left: 4px solid var(--sf-blue);
    padding: 12px 16px;
    border-radius: 8px;
}

div[data-testid="stMetric"] label {
    color: var(--sf-neutral) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--sf-mid-blue) !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] {
    border: 1px solid #E8F4FA !important;
    border-radius: 8px !important;
    border-left: 3px solid var(--sf-star-blue) !important;
    transition: border-color 0.2s ease;
}

[data-testid="stExpander"]:hover {
    border-color: var(--sf-blue) !important;
}

div.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    border-bottom: 2px solid #E8F4FA;
    overflow-x: auto;
}

div.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 18px;
    font-weight: 700;
    font-size: 0.88rem;
    white-space: nowrap;
    transition: background 0.2s ease;
}

div.stTabs [data-baseweb="tab"]:hover {
    background: #F0F8FF;
}

div.stTabs [aria-selected="true"] {
    border-bottom: 3px solid var(--sf-blue) !important;
    background: #F0F8FF;
}

.stCodeBlock {
    border-radius: 8px !important;
    border: 1px solid #E8F4FA !important;
}

[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-size: 0.92rem;
}

[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}

a { color: var(--sf-blue) !important; font-weight: 600; }
a:hover { color: var(--sf-mid-blue) !important; text-decoration: underline !important; }

.sf-hero-banner {
    background: linear-gradient(135deg, #11567F 0%, #29B5E8 50%, #71D3DC 100%);
    padding: 2.5rem 3rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.sf-hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: radial-gradient(circle, rgba(255,255,255,0.12) 1px, transparent 1px);
    background-size: 24px 24px;
    pointer-events: none;
}

.sf-hero-banner h2 {
    color: #FFFFFF !important;
    margin: 0 !important;
    font-size: 2rem !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.sf-hero-banner p {
    color: rgba(255,255,255,0.9) !important;
    margin: 0.5rem 0 0 0 !important;
    font-size: 1.15rem;
}

.sf-card {
    background: #FFFFFF;
    border: 1px solid #E8F4FA;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    transition: all 0.25s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.sf-card:hover {
    box-shadow: 0 6px 20px rgba(41, 181, 232, 0.12);
    border-color: #29B5E8;
    transform: translateY(-2px);
}

.sf-card-accent {
    border-left: 4px solid var(--sf-blue);
}

.sf-footer {
    text-align: center;
    padding: 1.5rem 0;
    margin-top: 3rem;
    border-top: 2px solid #E8F4FA;
    color: var(--sf-neutral);
    font-size: 0.85rem;
}

.sf-section-header {
    border-left: 4px solid var(--sf-blue);
    padding-left: 1rem;
    margin: 1rem 0;
}

.sf-big-text {
    font-size: 1.2rem;
    font-weight: 600;
    color: #11567F;
    line-height: 1.6;
}

.sf-timeline-item {
    display: flex;
    align-items: center;
    padding: 14px 18px;
    margin: 6px 0;
    border-radius: 0 10px 10px 0;
    background: #F8FBFF;
    transition: all 0.2s ease;
    gap: 0.5rem;
}

.sf-timeline-item:hover {
    background: #EBF7FD;
    transform: translateX(4px);
}

.sf-takeaway-card {
    background: #FFFFFF;
    border: 1px solid #E8F4FA;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: all 0.25s ease;
}

.sf-takeaway-card:hover {
    box-shadow: 0 6px 20px rgba(41, 181, 232, 0.12);
    border-color: #29B5E8;
    transform: translateY(-2px);
}

.sf-sidebar-brand {
    text-align: center;
    padding: 0.5rem 0 0.2rem 0;
}

.sf-sidebar-brand h3 {
    font-size: 1.1rem !important;
    color: #11567F !important;
    margin: 0 !important;
    letter-spacing: 0.5px;
}

.sf-sidebar-brand p {
    font-size: 0.75rem;
    color: #8A999E;
    margin: 0.15rem 0 0 0;
}

.sf-speaker-card {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 6px 0;
}

.sf-speaker-card .icon {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; color: white;
    flex-shrink: 0;
}

.sf-speaker-card .info {
    font-size: 0.82rem;
    color: #24323D;
    line-height: 1.3;
}

.sf-speaker-card .info small {
    color: #8A999E;
    font-size: 0.72rem;
}
</style>
"""

st.markdown(BRAND_CSS, unsafe_allow_html=True)

if hasattr(st, "navigation"):
    page = st.navigation(
        {
            "": [
                st.Page("app_pages/agenda.py", title=t("nav_agenda"), icon=":material/calendar_today:"),
            ],
            t("nav_deep_dives"): [
                st.Page("app_pages/deep_dive_1.py", title=t("nav_dd1"), icon=":material/database:"),
                st.Page("app_pages/deep_dive_2.py", title=t("nav_dd2"), icon=":material/psychology:"),
            ],
            t("nav_practical"): [
                st.Page("app_pages/lab_recursos.py", title=t("nav_lab"), icon=":material/science:"),
            ],
        },
        position="sidebar",
    )

    with st.sidebar:
        st.divider()
        st.radio("Language", ["PT", "EN"], index=0 if st.session_state.lang == "PT" else 1, key="_lang_radio", horizontal=True, on_change=_sync_lang)
        st.divider()
        st.markdown(f"""
<div class="sf-sidebar-brand">
    <h3>&#x2744; Snowflake</h3>
    <p>Partner Enablement &bull; Lisboa 2026</p>
</div>
""", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"**{t('sidebar_speakers')}**")
        st.markdown(f"""
<div class="sf-speaker-card"><div class="icon" style="background:#29B5E8;">PJ</div><div class="info">Pedro Jose<br><small>{t("pedro_role")}</small></div></div>
<div class="sf-speaker-card"><div class="icon" style="background:#7D44CF;">DT</div><div class="info">David Tinoco<br><small>{t("david_role")}</small></div></div>
<div class="sf-speaker-card"><div class="icon" style="background:#FF9F36;">FA</div><div class="info">Frederic Arendt<br><small>GTM & Partnerships</small></div></div>
""", unsafe_allow_html=True)
        st.divider()
        st.caption(t("sidebar_location"))
        st.caption("[snowflake.com](https://www.snowflake.com)")

    page.run()
else:
    import importlib
    import sys

    PAGES = {
        t("nav_agenda"): "app_pages.agenda",
        t("nav_dd1"): "app_pages.deep_dive_1",
        t("nav_dd2"): "app_pages.deep_dive_2",
        t("nav_lab"): "app_pages.lab_recursos",
    }

    with st.sidebar:
        st.markdown(f"""
<div class="sf-sidebar-brand">
    <h3>&#x2744; Snowflake</h3>
    <p>Partner Enablement &bull; Lisboa 2026</p>
</div>
""", unsafe_allow_html=True)
        st.divider()
        st.radio("Language", ["PT", "EN"], index=0 if st.session_state.lang == "PT" else 1, key="_lang_radio", horizontal=True, on_change=_sync_lang)
        st.divider()
        selection = st.radio("", list(PAGES.keys()), index=0)
        st.divider()
        st.markdown(f"**{t('sidebar_speakers')}**")
        st.markdown(f"""
<div class="sf-speaker-card"><div class="icon" style="background:#29B5E8;">PJ</div><div class="info">Pedro Jose<br><small>{t("pedro_role")}</small></div></div>
<div class="sf-speaker-card"><div class="icon" style="background:#7D44CF;">DT</div><div class="info">David Tinoco<br><small>{t("david_role")}</small></div></div>
<div class="sf-speaker-card"><div class="icon" style="background:#FF9F36;">FA</div><div class="info">Frederic Arendt<br><small>GTM & Partnerships</small></div></div>
""", unsafe_allow_html=True)
        st.divider()
        st.caption(t("sidebar_location"))
        st.caption("[snowflake.com](https://www.snowflake.com)")

    mod_name = PAGES[selection]
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    importlib.import_module(mod_name)

st.markdown(f"""
<div class="sf-footer">
    {t('footer')}<br>
    <span style="color: #29B5E8;">&#x2744;</span> snowflake.com
</div>
""", unsafe_allow_html=True)

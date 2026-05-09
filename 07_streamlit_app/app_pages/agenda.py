import streamlit as st

st.markdown("""
<div class="sf-hero-banner">
    <h2>&#x2744; Sessao de Capacitacao para Partners</h2>
    <p>Snowflake AI Data Cloud &mdash; Lisboa, Portugal</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p class="sf-big-text">
<strong>Objetivo:</strong> Proporcionar aos partners uma visao completa e pratica da plataforma,
permitindo <em>compreender</em>, <em>observar</em>, <em>experimentar</em> e definir proximos passos.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Agenda - 3 Horas")

agenda_items = [
    ("10:00 - 10:10", "10 min", "Boas-vindas e Objetivos", "Pedro Jose", "#29B5E8"),
    ("10:10 - 10:40", "30 min", "Visao Geral do Snowflake AI Data Cloud", "Pedro Jose", "#29B5E8"),
    ("10:40 - 11:15", "35 min", "Aprofundamento I: Fundamentos da Plataforma + Demo", "David Tinoco", "#11567F"),
    ("11:15 - 11:25", "10 min", "Intervalo", "---", "#8A999E"),
    ("11:25 - 11:55", "30 min", "Aprofundamento II: IA e Aplicacoes + Demo", "David Tinoco", "#7D44CF"),
    ("11:55 - 12:25", "30 min", "Laboratorio Pratico Guiado", "David Tinoco", "#FF9F36"),
    ("12:25 - 12:30", "5 min", "Pausa", "---", "#8A999E"),
    ("12:30 - 13:00", "30 min", "Conclusao e Percurso de Capacitacao", "Frederic Arendt", "#71D3DC"),
]

for time_slot, duration, session, speaker, color in agenda_items:
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

st.markdown("## O que vao levar desta sessao")

takeaways = [
    ("Compreensao clara", "Arquitetura e proposta de valor do Snowflake", "#29B5E8"),
    ("Experiencia pratica", "Laboratorio guiado com exercicios hands-on", "#FF9F36"),
    ("Capacidades de IA", "Cortex AI integrado nativamente na plataforma", "#7D44CF"),
    ("Roteiro de capacitacao", "Percurso personalizado para cada perfil tecnico", "#71D3DC"),
    ("Acoes concretas", "Proximos passos para os proximos 30-60 dias", "#11567F"),
    ("GTM conjunto", "Oportunidades de Go-To-Market com Snowflake", "#D45B90"),
]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3, col1, col2, col3]

for i, (title, desc, color) in enumerate(takeaways):
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
    st.markdown("### Publico-alvo")
    st.markdown("""
<div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Data Analysts</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Data Engineers</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Architects</span>
    <span style="background: #EBF7FD; color: #11567F; padding: 6px 14px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Tech Leaders</span>
</div>
""", unsafe_allow_html=True)

with col_b:
    st.markdown("### Pre-requisitos")
    st.markdown("""
- Computador com browser atualizado
- Conta trial Snowflake ([signup.snowflake.com](https://signup.snowflake.com))
- Conhecimentos basicos de SQL (recomendado)
""")

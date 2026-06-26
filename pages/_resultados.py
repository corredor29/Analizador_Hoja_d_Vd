import streamlit as st
from components.score_card import mostrar_score_card
from components.skills_chart import mostrar_skills_chart
from components.experience_timeline import mostrar_experience_timeline
from components.job_match_panel import mostrar_job_match_panel
from components.requisitos_panel import mostrar_requisitos_panel

st.set_page_config(page_title="Resultados", page_icon="📊")
st.title("📊 Resultados del análisis")

if "consenso" not in st.session_state:
    st.warning("⚠️ Primero debes analizar un CV.")
    st.stop()

consenso              = st.session_state["consenso"]
match                 = st.session_state.get("match")
evaluacion_requisitos = st.session_state.get("evaluacion_requisitos")

mostrar_score_card(consenso)
st.divider()
mostrar_requisitos_panel(evaluacion_requisitos)
st.divider()
mostrar_skills_chart(consenso)
st.divider()
mostrar_experience_timeline(consenso)
st.divider()
mostrar_job_match_panel(match)
import streamlit as st
from components.ia_comparison_panel import mostrar_ia_comparison_panel

st.set_page_config(page_title="Panel IAs", page_icon="🤖")
st.title("🤖 Panel de IAs")

if "consenso" not in st.session_state:
    st.warning("⚠️ Primero debes analizar un CV.")
    st.stop()

consenso = st.session_state["consenso"]

mostrar_ia_comparison_panel(consenso)

st.divider()
st.subheader("📋 Recomendaciones del consenso")
for rec in consenso.get("recomendaciones", []):
    st.markdown(f"- {rec}")
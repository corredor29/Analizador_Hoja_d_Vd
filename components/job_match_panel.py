import streamlit as st

def mostrar_job_match_panel(match: dict):
    """Muestra el panel de match entre el CV y la oferta de trabajo."""
    if not match:
        st.info("No se proporcionó oferta de trabajo para comparar.")
        return

    st.subheader("🎯 Match con la oferta")

    porcentaje = match.get("porcentaje_match", 0)
    nivel      = match.get("nivel_match", "")
    color      = _color_match(nivel)

    st.markdown(f"""
    <div style="
        background: {color};
        padding: 1rem 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    ">
        <h2 style="margin:0">{porcentaje}% de match</h2>
        <p style="margin:0">Nivel: <strong>{nivel}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("####")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**✅ Skills que coinciden:**")
        for skill in match.get("skills_match", []):
            st.markdown(f"- {skill}")

    with col2:
        st.markdown("**❌ Skills faltantes:**")
        for skill in match.get("skills_faltantes", []):
            st.markdown(f"- {skill}")

    # Desglose semántico (disponible cuando se usaron embeddings de Mistral)
    kw  = match.get("porcentaje_keywords")
    sem = match.get("porcentaje_semantico")
    if kw is not None and sem is not None:
        st.markdown("####")
        c1, c2 = st.columns(2)
        c1.metric("Keywords match", f"{kw}%")
        c2.metric("Similitud semántica (Mistral)", f"{sem}%")

    st.markdown("####")
    st.info(f"💡 {match.get('recomendacion', '')}")


def _color_match(nivel: str) -> str:
    return {
        "Alto":  "#2ecc71",
        "Medio": "#f39c12",
        "Bajo":  "#e74c3c",
    }.get(nivel, "#95a5a6")
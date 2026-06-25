import streamlit as st


def mostrar_experience_timeline(consenso: dict):
    """Muestra la experiencia laboral en formato timeline."""
    experiencia = consenso.get("experiencia", [])

    if not experiencia:
        st.warning("No se detectó experiencia laboral.")
        return

    st.subheader("💼 Experiencia laboral")

    for i, exp in enumerate(experiencia):
        cargo   = exp.get("cargo", "Cargo desconocido")
        empresa = exp.get("empresa", "Empresa desconocida")
        años    = exp.get("años", 0)

        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{cargo}** — {empresa}")
            col2.markdown(f"⏱️ {años} {'año' if años == 1 else 'años'}")

            if i < len(experiencia) - 1:
                st.markdown("---")
import streamlit as st


def mostrar_requisitos_panel(evaluacion: dict | None):
    """Muestra el panel de requisitos mínimos y razones de no contratación."""
    if not evaluacion:
        return

    cumple    = evaluacion.get("cumple", True)
    razones   = evaluacion.get("razones_no_contratado", [])
    evaluados = evaluacion.get("requisitos_evaluados", [])

    st.subheader("🚫 Requisitos mínimos")

    if cumple:
        st.markdown("""
        <div style="
            background: #2ecc71;
            padding: 1rem 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
        ">
            <h3 style="margin:0">✅ Candidato APTO</h3>
            <p style="margin:0">Cumple todos los requisitos mínimos del cargo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: #e74c3c;
            padding: 1rem 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
        ">
            <h3 style="margin:0">❌ Candidato NO CONTRATADO</h3>
            <p style="margin:0">No cumple {len(razones)} requisito(s) mínimo(s).</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Por qué no fue contratado:")
        for razon in razones:
            st.error(f"✗ {razon}")

    if evaluados:
        with st.expander("Ver detalle de cada requisito"):
            for req in evaluados:
                icono = "✅" if req["cumple"] else "❌"
                color = "green" if req["cumple"] else "red"
                st.markdown(
                    f"**{icono} {req['requisito']}**  \n"
                    f"<span style='color:{color}'>{req['detalle']}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown("---")

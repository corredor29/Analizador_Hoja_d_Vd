import streamlit as st
import pandas as pd


def mostrar_ia_comparison_panel(consenso: dict):
    """Muestra la tabla comparativa de resultados por IA."""
    st.subheader("🤖 Análisis por IA")

    scores_por_ia = consenso.get("scores_por_ia", {})

    if not scores_por_ia:
        st.warning("No hay resultados por IA disponibles.")
        return

    iconos = {"Claude": "🟣", "OpenAI": "🟢", "Gemini": "🔵", "Mistral": "🟠"}

    filas = []
    for ia, score in scores_por_ia.items():
        filas.append({
            "IA":    f"{iconos.get(ia, '⚪')} {ia}",
            "Score": score,
        })

    # Fila de consenso
    filas.append({
        "IA":    "✅ Consenso Final",
        "Score": consenso.get("score_final", 0),
    })

    df = pd.DataFrame(filas)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("####")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**💪 Fortalezas (consenso):**")
        for f in consenso.get("fortalezas", []):
            st.markdown(f"- {f}")

    with col2:
        st.markdown("**⚠️ Debilidades (consenso):**")
        for d in consenso.get("debilidades", []):
            st.markdown(f"- {d}")
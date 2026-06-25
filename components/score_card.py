import streamlit as st


def mostrar_score_card(consenso: dict):
    """Muestra la tarjeta con el score final y nivel del candidato."""
    score = consenso.get("score_final", 0)
    nivel = consenso.get("nivel", "N/A")

    color = _color_score(score)

    st.markdown(f"""
    <div style="
        background: {color};
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
    ">
        <h1 style="font-size: 4rem; margin: 0;">{score}</h1>
        <p style="font-size: 1.2rem; margin: 0;">Score Final</p>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <h3 style="margin: 0;">🎯 Nivel: {nivel}</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("####")

    col1, col2, col3 = st.columns(3)
    col1.metric("🟣 Claude",  f"{consenso.get('scores_por_ia', {}).get('Claude', 0):.1f}")
    col2.metric("🟢 OpenAI",  f"{consenso.get('scores_por_ia', {}).get('OpenAI', 0):.1f}")
    col3.metric("🔵 Gemini",  f"{consenso.get('scores_por_ia', {}).get('Gemini', 0):.1f}")

    nivel_acuerdo = consenso.get("nivel_acuerdo", "")
    ia_alta = consenso.get("ia_mas_alta", "")
    ia_baja = consenso.get("ia_mas_baja", "")

    st.info(f"📊 Nivel de acuerdo entre IAs: **{nivel_acuerdo}** | Mayor score: **{ia_alta}** | Menor score: **{ia_baja}**")


def _color_score(score: float) -> str:
    if score >= 75:
        return "#2ecc71" 
    elif score >= 50:
        return "#f39c12"  
    else:
        return "#e74c3c"  
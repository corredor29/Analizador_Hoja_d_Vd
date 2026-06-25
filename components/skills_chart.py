import streamlit as st
import plotly.express as px


def mostrar_skills_chart(consenso: dict):
    """Muestra la gráfica de habilidades detectadas."""
    skills = consenso.get("skills", [])

    if not skills:
        st.warning("No se detectaron habilidades.")
        return

    st.subheader("🛠️ Habilidades detectadas")

    fig = px.bar(
        x=[1] * len(skills),
        y=skills,
        orientation="h",
        color=skills,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis_title="",
        height=max(300, len(skills) * 30),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(" ".join([f"`{s}`" for s in skills]))
import streamlit as st
from src.analyzers import analizar_cv
from src.scorers import calcular_match, evaluar_requisitos_minimos
from src.reporters import guardar_resultado
from database.connection import get_session
from database.repositories.candidato_repository import crear_candidato
from database.repositories.analisis_repository import crear_analisis

st.set_page_config(page_title="Analizar", page_icon="🔍")
st.title("🔍 Analizar CV")

if "cv_texto" not in st.session_state:
    st.warning("⚠️ Primero debes subir un CV en la página anterior.")
    st.stop()

cv_texto           = st.session_state["cv_texto"]
contacto           = st.session_state["contacto"]
oferta_trabajo     = st.session_state.get("oferta_trabajo")
requisitos_minimos = st.session_state.get("requisitos_minimos")

st.markdown(f"**Archivo:** {st.session_state.get('archivo_nombre', '')}")
st.markdown(f"**Candidato:** {contacto.get('nombre', 'Desconocido')} | {contacto.get('email', '')}")

if st.button("🚀 Iniciar análisis multi-IA", type="primary", use_container_width=True):

    with st.status("Analizando CV con múltiples IAs...", expanded=True) as status:

        st.write("🟢 Consultando OpenAI...")
        st.write("🟠 Consultando Mistral...")

        consenso = analizar_cv(cv_texto, oferta_trabajo)

        st.write("⚖️ Calculando consenso...")

        match = None
        if oferta_trabajo:
            st.write("🎯 Calculando match con oferta...")
            match = calcular_match(consenso, oferta_trabajo)

        evaluacion_requisitos = None
        if requisitos_minimos:
            st.write("🚫 Evaluando requisitos mínimos...")
            evaluacion_requisitos = evaluar_requisitos_minimos(requisitos_minimos, consenso)

        st.write("💾 Guardando en base de datos...")
        with get_session() as session:
            candidato = crear_candidato(
                session,
                nombre=contacto.get("nombre") or "Desconocido",
                email=contacto.get("email") or "sin@email.com",
            )
            crear_analisis(
                session,
                candidato_id=candidato.id,
                skills=consenso.get("skills", []),
                experiencia=consenso.get("experiencia", []),
                score_openai=consenso.get("scores_por_ia", {}).get("OpenAI", 0),
                score_mistral=consenso.get("scores_por_ia", {}).get("Mistral", 0),
                score_final=consenso.get("score_final", 0),
            )

        st.write("📁 Guardando reporte JSON...")
        guardar_resultado(contacto, consenso, {}, match)

        status.update(label="✅ Análisis completado", state="complete")

    # Guardamos en sesión para la página de resultados
    st.session_state["consenso"]              = consenso
    st.session_state["match"]                 = match
    st.session_state["evaluacion_requisitos"] = evaluacion_requisitos

    st.success("✅ Análisis completado. Ve a **Resultados** para ver el informe.")
import streamlit as st
from components.upload_zone import mostrar_upload_zone
from src.extractors import extraer_texto, extraer_contacto

st.set_page_config(page_title="Subir CV", page_icon="📄")
st.title("📄 Subir CV")

archivo, oferta_trabajo, requisitos_minimos = mostrar_upload_zone()

if archivo:
    extension = archivo.name.split(".")[-1].lower()

    with st.spinner("Extrayendo texto del CV..."):
        cv_texto  = extraer_texto(archivo, extension)
        contacto  = extraer_contacto(archivo, extension)

    # Guardamos en sesión para las otras páginas
    st.session_state["cv_texto"]           = cv_texto
    st.session_state["contacto"]           = contacto
    st.session_state["oferta_trabajo"]     = oferta_trabajo
    st.session_state["requisitos_minimos"] = requisitos_minimos
    st.session_state["archivo_nombre"]     = archivo.name

    st.success("✅ CV cargado correctamente")

    with st.expander("👤 Datos de contacto detectados"):
        st.json(contacto)

    with st.expander("📝 Texto extraído"):
        st.text(cv_texto[:1000] + "..." if len(cv_texto) > 1000 else cv_texto)

    st.info("➡️ Ve a la página **Analizar** para continuar")
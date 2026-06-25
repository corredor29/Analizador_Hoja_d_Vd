import streamlit as st
from config.settings import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB


def mostrar_upload_zone() -> tuple:
    """
    Muestra el componente de carga de archivos y campo de oferta de trabajo.

    Returns:
        (archivo, oferta_trabajo) o (None, None) si no se subió nada
    """
    st.subheader("📄 Sube el CV")

    archivo = st.file_uploader(
        label="Arrastra o selecciona un archivo",
        type=ALLOWED_EXTENSIONS,
        help=f"Formatos permitidos: {', '.join(ALLOWED_EXTENSIONS)} | Máximo {MAX_FILE_SIZE_MB}MB",
    )

    if archivo:
        # Validar tamaño
        if archivo.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(f"❌ El archivo supera el límite de {MAX_FILE_SIZE_MB}MB")
            return None, None

        st.success(f"✅ Archivo cargado: **{archivo.name}** ({round(archivo.size / 1024, 1)} KB)")

    st.divider()
    st.subheader("💼 Oferta de trabajo (opcional)")

    oferta_trabajo = st.text_area(
        label="Pega aquí la descripción del cargo",
        placeholder="Ej: Se busca desarrollador Python con experiencia en Django, PostgreSQL y AWS...",
        height=150,
        help="Si ingresas la oferta, el análisis incluirá qué tan bien encaja el candidato con el cargo.",
    )

    return archivo, oferta_trabajo if oferta_trabajo.strip() else None
import streamlit as st
from database.connection import init_db, check_connection

st.set_page_config(
    page_title="CV Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inicializar base de datos ─────────────────────────────
@st.cache_resource
def inicializar_db():
    init_db()

inicializar_db()

if not check_connection():
    st.error("❌ No se pudo conectar a PostgreSQL. Verifica tu secrets.toml.")
    st.stop()

# ── Página principal ──────────────────────────────────────
st.title("📋 CV Analyzer")
st.markdown("Analizador de hojas de vida con múltiples IAs y consenso inteligente.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.info("**📄 Paso 1**\nSube el CV en PDF o DOCX")
col2.info("**🔍 Paso 2**\nAnaliza con OpenAI y Mistral")
col3.info("**📊 Paso 3**\nRevisa los resultados y el score final")
col4.info("**🤖 Paso 4**\nCompara qué dijo cada IA")

st.divider()
st.markdown("👈 Usa el menú lateral para navegar entre las páginas.")
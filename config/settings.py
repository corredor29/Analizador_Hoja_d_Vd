import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY    = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY   = os.getenv("MISTRAL_API_KEY")

WEIGHT_CLAUDE  = float(os.getenv("WEIGHT_CLAUDE",  0.40))
WEIGHT_OPENAI  = float(os.getenv("WEIGHT_OPENAI",  0.40))
WEIGHT_GEMINI  = float(os.getenv("WEIGHT_GEMINI",  0.20))
WEIGHT_MISTRAL = float(os.getenv("WEIGHT_MISTRAL", 0.00))

DB_HOST     = st.secrets["postgres"]["host"]
DB_PORT     = st.secrets["postgres"]["port"]
DB_NAME     = st.secrets["postgres"]["dbname"]
DB_USER     = st.secrets["postgres"]["user"]
DB_PASSWORD = st.secrets["postgres"]["password"]
DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── Configuración general (desde .env) ───────────────────
MAX_TOKENS         = int(os.getenv("MAX_TOKENS", 2000))
LANGUAGE           = os.getenv("LANGUAGE", "es")
UPLOAD_FOLDER      = os.getenv("UPLOAD_FOLDER", "data/uploads")
RESULTS_FOLDER     = os.getenv("RESULTS_FOLDER", "data/results")
ALLOWED_EXTENSIONS = ["pdf", "docx"]
MAX_FILE_SIZE_MB   = 10
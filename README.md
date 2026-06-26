# Analizador de Hoja de Vida

Aplicación web en **Streamlit** que analiza CVs (PDF/DOCX) usando múltiples modelos de IA en simultáneo (OpenAI GPT-4o + Mistral) y combina sus resultados con un sistema de consenso ponderado.

## Características

- Extracción de texto de CVs en formato PDF y DOCX
- Análisis multi-IA con consenso ponderado (60% OpenAI · 40% Mistral)
- Detección de skills, experiencia, fortalezas, debilidades y nivel (Junior/Mid/Senior)
- Matching con oferta de trabajo y evaluación de requisitos mínimos
- Persistencia de resultados en PostgreSQL
- Visualizaciones interactivas con Plotly

## Requisitos previos

- Python 3.11+
- PostgreSQL corriendo en `localhost:5432`
- API keys de OpenAI y Mistral

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd Analizador_Hoja_d_Vd

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Configuración

**1. Variables de entorno** — crea un archivo `.env` en la raíz basándote en `.env.example`:

```env
OPENAI_API_KEY=sk-proj-...
MISTRAL_API_KEY=...

# Pesos de consenso (deben sumar 1.0)
WEIGHT_OPENAI=0.60
WEIGHT_MISTRAL=0.40

MAX_TOKENS=2000
LANGUAGE=es
UPLOAD_FOLDER=data/uploads
RESULTS_FOLDER=data/results
```

**2. Secretos de Streamlit** — crea `~/.streamlit/secrets.toml`:

```toml
[postgres]
host     = "localhost"
port     = 5432
dbname   = "cv_analyzer"
user     = "postgres"
password = "tu_password"
```

**3. Base de datos** — crea la base de datos en PostgreSQL:

```sql
CREATE DATABASE cv_analyzer;
```

Las tablas se crean automáticamente al iniciar la aplicación.

## Uso

```bash
streamlit run app.py
```

La app queda disponible en `http://localhost:8501`.

### Flujo de trabajo

| Paso | Página | Descripción |
|------|--------|-------------|
| 1 | **Subir CV** | Sube un PDF o DOCX; se extrae texto y datos de contacto |
| 2 | **Analizar** | Las IAs analizan el CV y generan un consenso |
| 3 | **Resultados** | Visualiza score, skills, experiencia y match con la oferta |
| 4 | **Panel IAs** | Compara las respuestas individuales de cada modelo |

## Estructura del proyecto

```
├── app.py                  # Página principal y punto de entrada
├── pages/                  # Páginas de la app (Streamlit MPA)
│   ├── _subir_cv.py
│   ├── _analizar.py
│   ├── _resultados.py
│   └── _panel_ia.py
├── src/
│   ├── analyzers/          # Orquestador multi-IA y lógica de consenso
│   │   ├── providers/      # Implementaciones de OpenAI y Mistral
│   │   └── consensus/      # Agregación y scoring ponderado
│   ├── extractors/         # Extracción de texto desde PDF y DOCX
│   ├── scorers/            # Scoring del CV y matching con ofertas
│   ├── parsers/            # Parseo de secciones y contacto
│   └── reporters/          # Exportación de resultados a JSON
├── components/             # Componentes Streamlit reutilizables
├── database/               # Modelos ORM y repositorios (PostgreSQL)
├── config/
│   └── settings.py         # Carga de variables de entorno y secretos
├── data/
│   ├── uploads/            # CVs subidos temporalmente
│   └── results/            # Reportes JSON generados
└── requirements.txt
```

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| UI | Streamlit |
| LLMs | OpenAI GPT-4o, Mistral Large (vía LangChain) |
| Extracción PDF | pdfplumber |
| Extracción DOCX | python-docx |
| Base de datos | PostgreSQL + SQLAlchemy |
| Visualización | Plotly |
| Configuración | python-dotenv + Streamlit secrets |

## Desarrollo

```bash
# Ejecutar tests
pytest

# Formatear código
black .

# Lint
ruff check .
```

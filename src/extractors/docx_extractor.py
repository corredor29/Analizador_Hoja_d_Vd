import re
from docx import Document
from src.extractors.pdf_extractor import limpiar_texto, extraer_contacto_desde_texto


def extraer_texto_docx(archivo) -> str:
    """
    Extrae todo el texto de un archivo Word (.docx).
    'archivo' puede ser una ruta (str) o un objeto de bytes (Streamlit UploadedFile).
    """
    documento = Document(archivo)
    texto = ""

    for parrafo in documento.paragraphs:
        if parrafo.text.strip():
            texto += parrafo.text + "\n"

    for tabla in documento.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                if celda.text.strip():
                    texto += celda.text + "\n"

    return limpiar_texto(texto)


def extraer_contacto_docx(archivo) -> dict:
    """Extrae email y teléfono de un archivo Word."""
    texto = extraer_texto_docx(archivo)
    return extraer_contacto_desde_texto(texto)
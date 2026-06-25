from src.extractors.pdf_extractor import extraer_texto_pdf, extraer_contacto_pdf
from src.extractors.docx_extractor import extraer_texto_docx, extraer_contacto_docx


def extraer_texto(archivo, extension: str) -> str:
    """
    Extrae texto de un CV según su extensión.
    Uso: extraer_texto(archivo, "pdf") o extraer_texto(archivo, "docx")
    """
    if extension == "pdf":
        return extraer_texto_pdf(archivo)
    elif extension == "docx":
        return extraer_texto_docx(archivo)
    else:
        raise ValueError(f"Formato no soportado: {extension}")


def extraer_contacto(archivo, extension: str) -> dict:
    """Extrae contacto de un CV según su extensión."""
    if extension == "pdf":
        return extraer_contacto_pdf(archivo)
    elif extension == "docx":
        return extraer_contacto_docx(archivo)
    else:
        raise ValueError(f"Formato no soportado: {extension}")
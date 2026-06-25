import pdfplumber
import re


def extraer_texto_pdf(archivo) -> str:
    """
    Extrae todo el texto de un PDF.
    'archivo' puede ser una ruta (str) o un objeto de bytes (Streamlit UploadedFile).
    """
    texto = ""

    with pdfplumber.open(archivo) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()
            if contenido:
                texto += contenido + "\n"

    return limpiar_texto(texto)


def limpiar_texto(texto: str) -> str:
    """Limpia el texto extraído eliminando caracteres innecesarios."""
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = "\n".join(linea.strip() for linea in texto.splitlines())
    texto = re.sub(r" {2,}", " ", texto)

    return texto.strip()


def extraer_contacto_pdf(archivo) -> dict:
    """
    Extrae email y teléfono del PDF usando expresiones regulares.
    Retorna un diccionario con los datos encontrados.
    """
    texto = extraer_texto_pdf(archivo)
    return extraer_contacto_desde_texto(texto)


def extraer_contacto_desde_texto(texto: str) -> dict:
    """Extrae email y teléfono de un texto con regex."""
    email = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", texto)
    telefono = re.findall(r"[\+]?[\d\s\-\(\)]{7,15}", texto)

    return {
        "email": email[0] if email else None,
        "telefono": telefono[0].strip() if telefono else None,
    }
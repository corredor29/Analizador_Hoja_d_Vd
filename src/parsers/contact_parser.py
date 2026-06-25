import re


def parsear_contacto(cv_texto: str) -> dict:
    return {
        "nombre":   _extraer_nombre(cv_texto),
        "email":    _extraer_email(cv_texto),
        "telefono": _extraer_telefono(cv_texto),
        "linkedin": _extraer_linkedin(cv_texto),
        "github":   _extraer_github(cv_texto),
    }


def _extraer_email(texto: str) -> str | None:
    resultado = re.findall(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", texto
    )
    return resultado[0] if resultado else None


def _extraer_telefono(texto: str) -> str | None:
    resultado = re.findall(
        r"[\+]?[\d\s\-\(\)]{7,15}", texto
    )
    return resultado[0].strip() if resultado else None


def _extraer_linkedin(texto: str) -> str | None:
    resultado = re.findall(
        r"linkedin\.com/in/[a-zA-Z0-9\-\_]+", texto
    )
    return resultado[0] if resultado else None


def _extraer_github(texto: str) -> str | None:
    resultado = re.findall(
        r"github\.com/[a-zA-Z0-9\-\_]+", texto
    )
    return resultado[0] if resultado else None


def _extraer_nombre(texto: str) -> str | None:
    """
    Intenta extraer el nombre de las primeras líneas del CV,
    donde normalmente aparece el nombre del candidato.
    """
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    for linea in lineas[:5]:
        if re.search(r"[@://\d]{3,}", linea):
            continue
        if 3 <= len(linea.split()) <= 5:
            return linea
    return None
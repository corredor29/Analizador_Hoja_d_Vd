import re

SECCIONES = {
    "experiencia": [
        "experiencia", "experience", "trabajo", "empleo",
        "historial laboral", "trayectoria", "cargo", "posición"
    ],
    "educacion": [
        "educación", "education", "formación", "estudios",
        "académico", "universidad", "título", "grado"
    ],
    "skills": [
        "habilidades", "skills", "competencias", "tecnologías",
        "herramientas", "conocimientos", "lenguajes"
    ],
    "idiomas": [
        "idiomas", "languages", "lenguas"
    ],
    "certificaciones": [
        "certificaciones", "certifications", "cursos", "courses", "diplomas"
    ],
    "proyectos": [
        "proyectos", "projects", "portafolio", "portfolio"
    ],
    "resumen": [
        "resumen", "summary", "perfil", "profile", "sobre mí", "about me", "objetivo"
    ],
}


def parsear_secciones(cv_texto: str) -> dict:
    """
    Divide el texto del CV en secciones identificadas.

    Returns:
        {
            "resumen": "Texto del resumen...",
            "experiencia": "Texto de experiencia...",
            "educacion": "Texto de educación...",
            "skills": "Texto de habilidades...",
            "idiomas": "Texto de idiomas...",
            "certificaciones": "Texto de certificaciones...",
            "proyectos": "Texto de proyectos...",
            "otros": "Texto no clasificado...",
        }
    """
    lineas = cv_texto.splitlines()
    secciones_encontradas = {}
    seccion_actual = "otros"
    buffer = []

    for linea in lineas:
        linea_lower = linea.lower().strip()
        seccion_detectada = _detectar_seccion(linea_lower)

        if seccion_detectada:
            if buffer:
                secciones_encontradas[seccion_actual] = "\n".join(buffer).strip()
            seccion_actual = seccion_detectada
            buffer = []
        else:
            if linea.strip():
                buffer.append(linea)

    if buffer:
        secciones_encontradas[seccion_actual] = "\n".join(buffer).strip()

    return secciones_encontradas


def _detectar_seccion(linea: str) -> str | None:
    """Detecta si una línea es un encabezado de sección."""
    for nombre_seccion, palabras_clave in SECCIONES.items():
        for palabra in palabras_clave:
            if palabra in linea:
                return nombre_seccion
    return None


def obtener_seccion(secciones: dict, nombre: str) -> str:
    """Retorna el texto de una sección o cadena vacía si no existe."""
    return secciones.get(nombre, "")
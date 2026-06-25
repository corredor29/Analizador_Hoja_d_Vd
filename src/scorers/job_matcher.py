def calcular_match(consenso: dict, oferta_trabajo: str) -> dict:
    oferta_lower  = oferta_trabajo.lower()
    skills_cv     = [s.lower() for s in consenso.get("skills", [])]

    skills_match    = [s for s in skills_cv if s in oferta_lower]
    skills_faltantes = _detectar_skills_faltantes(oferta_lower, skills_cv)

    # Porcentaje de skills del CV que aparecen en la oferta
    if skills_cv:
        porcentaje = round(len(skills_match) / len(skills_cv) * 100, 1)
    else:
        porcentaje = 0.0

    nivel_match = _nivel_match(porcentaje)

    return {
        "porcentaje_match":  porcentaje,
        "nivel_match":       nivel_match,
        "skills_match":      skills_match,
        "skills_faltantes":  skills_faltantes,
        "recomendacion":     _generar_recomendacion(porcentaje, skills_faltantes),
    }


def _detectar_skills_faltantes(oferta: str, skills_cv: list[str]) -> list[str]:
    """Detecta skills mencionadas en la oferta que no tiene el candidato."""
    skills_comunes = [
        "python", "java", "javascript", "sql", "docker", "kubernetes",
        "aws", "azure", "gcp", "react", "angular", "node", "git",
        "postgresql", "mongodb", "redis", "linux", "scrum", "agile",
        "machine learning", "deep learning", "tensorflow", "pytorch",
    ]
    faltantes = [
        skill for skill in skills_comunes
        if skill in oferta and skill not in skills_cv
    ]
    return faltantes


def _nivel_match(porcentaje: float) -> str:
    if porcentaje >= 75:
        return "Alto"
    elif porcentaje >= 50:
        return "Medio"
    else:
        return "Bajo"


def _generar_recomendacion(porcentaje: float, faltantes: list[str]) -> str:
    if porcentaje >= 75:
        msg = "El candidato encaja muy bien con el cargo."
    elif porcentaje >= 50:
        msg = "El candidato cumple varios requisitos del cargo."
    else:
        msg = "El candidato no cumple suficientes requisitos del cargo."

    if faltantes:
        msg += f" Le faltan: {', '.join(faltantes[:3])}."

    return msg
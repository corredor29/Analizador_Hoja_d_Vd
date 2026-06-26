import re


def evaluar_requisitos_minimos(requisitos_texto: str, consenso: dict) -> dict:
    """
    Evalúa si el candidato cumple los requisitos mínimos eliminatorios.

    Returns:
        {
          "cumple": bool,
          "razones_no_contratado": list[str],   # motivos de descarte
          "requisitos_evaluados": list[dict],   # detalle req por req
        }
    """
    lineas = [l.strip(" -•*·") for l in requisitos_texto.splitlines() if l.strip()]
    if not lineas:
        return {"cumple": True, "razones_no_contratado": [], "requisitos_evaluados": []}

    skills_candidato = [s.lower() for s in consenso.get("skills", [])]
    nivel_candidato  = consenso.get("nivel", "").lower()
    experiencia      = consenso.get("experiencia", [])
    años_candidato   = sum(exp.get("años", 0) for exp in experiencia)

    evaluados = []
    razones   = []

    for linea in lineas:
        linea_lower = linea.lower()
        cumple_req, descripcion = _evaluar_linea(
            linea_lower, skills_candidato, nivel_candidato, años_candidato
        )
        evaluados.append({"requisito": linea, "cumple": cumple_req, "detalle": descripcion})
        if not cumple_req:
            razones.append(descripcion)

    return {
        "cumple":                 len(razones) == 0,
        "razones_no_contratado":  razones,
        "requisitos_evaluados":   evaluados,
    }


def _evaluar_linea(linea: str, skills: list[str], nivel: str, años: float) -> tuple[bool, str]:
    """Evalúa una sola línea de requisito. Retorna (cumple, descripcion)."""

    # ── Años de experiencia ───────────────────────────────────────
    match_años = re.search(r"(\d+)\s*a[ñn]os?\s+de\s+experiencia", linea)
    if match_años or ("años" in linea and "experiencia" in linea):
        if match_años:
            requeridos = int(match_años.group(1))
        else:
            nums = re.findall(r"\d+", linea)
            requeridos = int(nums[0]) if nums else 1
        if años >= requeridos:
            return True, f"Experiencia: {años:.0f} años (requiere {requeridos})"
        return False, f"Experiencia insuficiente: tiene {años:.0f} años, se requieren {requeridos}"

    # ── Nivel (Junior / Mid / Senior) ────────────────────────────
    nivel_map = {"junior": 1, "mid": 2, "senior": 3}
    for kw, val in nivel_map.items():
        if kw in linea:
            val_candidato = nivel_map.get(nivel, 0)
            if val_candidato >= val:
                return True, f"Nivel: {nivel.capitalize()} (requiere {kw.capitalize()})"
            return False, f"Nivel insuficiente: el candidato es {nivel.capitalize() or 'desconocido'}, se requiere {kw.capitalize()}"

    # ── Idiomas ───────────────────────────────────────────────────
    idiomas = {"inglés": "english", "ingles": "english", "english": "english",
               "francés": "french", "frances": "french", "french": "french",
               "portugués": "portuguese", "portugues": "portuguese"}
    for kw_es, kw_en in idiomas.items():
        if kw_es in linea or kw_en in linea:
            if kw_en in skills or kw_es in skills or any(kw_en in s or kw_es in s for s in skills):
                return True, f"Idioma '{kw_es}' presente en el CV"
            return False, f"No se detectó '{kw_es}' en el CV del candidato"

    # ── Skills / tecnologías ──────────────────────────────────────
    tecnologias_conocidas = [
        "python", "java", "javascript", "typescript", "sql", "docker",
        "kubernetes", "aws", "azure", "gcp", "react", "angular", "vue",
        "node", "nodejs", "git", "postgresql", "mysql", "mongodb", "redis",
        "linux", "scrum", "agile", "machine learning", "deep learning",
        "tensorflow", "pytorch", "django", "fastapi", "flask", "spring",
        "c++", "c#", "go", "rust", "php", "ruby", "scala", "kotlin",
        "swift", "r", "hadoop", "spark", "kafka", "terraform", "ansible",
    ]
    for tech in tecnologias_conocidas:
        if tech in linea:
            if tech in skills:
                return True, f"Skill '{tech}' presente en el CV"
            return False, f"Skill obligatoria '{tech}' no encontrada en el CV"

    # ── Educación / título ────────────────────────────────────────
    palabras_educacion = ["título", "titulo", "grado", "pregrado", "licenciatura",
                          "maestría", "maestria", "doctorado", "ingeniería", "ingenieria",
                          "universidad", "técnico", "tecnico", "certificación", "certificacion"]
    for kw in palabras_educacion:
        if kw in linea:
            # No tenemos educación en el modelo actual; indicamos que no se pudo verificar
            return False, f"No se pudo verificar requisito educativo: '{linea}' (no está en el CV analizado)"

    # ── Requisito genérico no reconocido ─────────────────────────
    return False, f"No se pudo verificar: '{linea}' (no detectado automáticamente)"


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
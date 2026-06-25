from src.analyzers.providers.base_analyzer import ResultadoAnalisis


def calcular_score_cv(resultado: ResultadoAnalisis) -> dict:
    score_experiencia  = _score_experiencia(resultado.experiencia)
    score_skills       = _score_skills(resultado.skills)
    score_completitud  = _score_completitud(resultado)

    desglose = {
        "experiencia": score_experiencia,
        "skills":      score_skills,
        "completitud": score_completitud,
    }

    score_total = round(
        score_experiencia * 0.40 +
        score_skills      * 0.35 +
        score_completitud * 0.25,
        1
    )

    return {
        "score_total":  score_total,
        "desglose":     desglose,
        "nivel":        resultado.nivel,
        "fortalezas":   resultado.fortalezas,
        "debilidades":  resultado.debilidades,
        "recomendaciones": resultado.recomendaciones,
    }


def _score_experiencia(experiencia: list[dict]) -> float:
    """Puntúa la experiencia según años y cantidad de cargos."""
    if not experiencia:
        return 0.0

    total_años = sum(exp.get("años", 0) for exp in experiencia)
    cantidad   = len(experiencia)

    if total_años >= 10:
        base = 100
    elif total_años >= 5:
        base = 80
    elif total_años >= 3:
        base = 60
    elif total_años >= 1:
        base = 40
    else:
        base = 20

    # Bonus por variedad de cargos (máx 10 puntos)
    bonus = min(cantidad * 2, 10)
    return min(base + bonus, 100)


def _score_skills(skills: list[str]) -> float:
    """Puntúa según la cantidad de skills detectadas."""
    cantidad = len(skills)
    if cantidad >= 15:
        return 100
    elif cantidad >= 10:
        return 80
    elif cantidad >= 5:
        return 60
    elif cantidad >= 2:
        return 40
    else:
        return 20


def _score_completitud(resultado: ResultadoAnalisis) -> float:
    """Puntúa qué tan completo está el CV."""
    puntos = 0
    if resultado.skills:        puntos += 25
    if resultado.experiencia:   puntos += 25
    if resultado.fortalezas:    puntos += 25
    if resultado.resumen:       puntos += 25
    return float(puntos)
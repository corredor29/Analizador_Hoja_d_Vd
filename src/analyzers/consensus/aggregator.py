from src.analyzers.providers.base_analyzer import ResultadoAnalisis
from config.settings import WEIGHT_CLAUDE, WEIGHT_OPENAI, WEIGHT_GEMINI, WEIGHT_MISTRAL


def agregar_resultados(resultados: list[ResultadoAnalisis]) -> dict:
    """
    Combina los resultados de todas las IAs en un consenso final.

    Args:
        resultados: Lista de ResultadoAnalisis de cada IA

    Returns:
        Diccionario con el análisis consolidado
    """
    if not resultados:
        raise ValueError("No hay resultados de IAs para agregar")

    pesos = {
        "Claude":  WEIGHT_CLAUDE,
        "OpenAI":  WEIGHT_OPENAI,
        "Gemini":  WEIGHT_GEMINI,
        "Mistral": WEIGHT_MISTRAL,
    }

    score_final = 0.0
    peso_total = 0.0

    for resultado in resultados:
        peso = pesos.get(resultado.ia_nombre, 0)
        score_final += resultado.score * peso
        peso_total += peso

    # Si los pesos no suman 1, normalizamos
    if peso_total > 0:
        score_final = score_final / peso_total

    # ── Skills únicas (unión de todas las IAs) ────────────
    skills_union = list(set(
        skill
        for resultado in resultados
        for skill in resultado.skills
    ))

    # ── Experiencia consolidada ───────────────────────────
    experiencia_consolidada = _consolidar_experiencia(resultados)

    # ── Fortalezas donde coinciden al menos 2 IAs ─────────
    fortalezas_consenso = _encontrar_consenso(
        [r.fortalezas for r in resultados]
    )

    # ── Debilidades donde coinciden al menos 2 IAs ────────
    debilidades_consenso = _encontrar_consenso(
        [r.debilidades for r in resultados]
    )

    # ── Nivel por mayoría ─────────────────────────────────
    niveles = [r.nivel for r in resultados]
    nivel_final = max(set(niveles), key=niveles.count)

    # ── Scores individuales por IA ────────────────────────
    scores_por_ia = {r.ia_nombre: r.score for r in resultados}

    return {
        "score_final": round(score_final, 1),
        "scores_por_ia": scores_por_ia,
        "skills": skills_union,
        "experiencia": experiencia_consolidada,
        "fortalezas": fortalezas_consenso,
        "debilidades": debilidades_consenso,
        "nivel": nivel_final,
        "total_ias": len(resultados),
    }


def _consolidar_experiencia(resultados: list[ResultadoAnalisis]) -> list[dict]:
    """Toma la experiencia de la IA con mayor score."""
    mejor = max(resultados, key=lambda r: r.score)
    return mejor.experiencia


def _encontrar_consenso(listas: list[list[str]], min_coincidencias: int = 2) -> list[str]:
    """
    Retorna los items que aparecen en al menos 'min_coincidencias' listas.
    Si no hay suficientes coincidencias, retorna todos los items únicos.
    """
    conteo = {}
    for lista in listas:
        for item in lista:
            conteo[item] = conteo.get(item, 0) + 1

    consenso = [item for item, cnt in conteo.items() if cnt >= min_coincidencias]

    return consenso if consenso else list(conteo.keys())
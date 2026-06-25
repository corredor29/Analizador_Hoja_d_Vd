from src.analyzers.providers.base_analyzer import ResultadoAnalisis
from config.settings import WEIGHT_CLAUDE, WEIGHT_OPENAI, WEIGHT_GEMINI, WEIGHT_MISTRAL


def calcular_score_consenso(resultados: list[ResultadoAnalisis]) -> dict:
    """
    Calcula el score final ponderado y métricas de acuerdo entre IAs.

    Returns:
        {
            "score_final": 81.5,
            "scores_por_ia": {"Claude": 82, "OpenAI": 78, ...},
            "nivel_acuerdo": "Alto",     # Alto | Medio | Bajo
            "varianza": 4.5,             # Qué tan distintos fueron los scores
            "ia_mas_alta": "Gemini",
            "ia_mas_baja": "OpenAI",
        }
    """
    if not resultados:
        raise ValueError("No hay resultados para calcular el score")

    pesos = {
        "Claude":  WEIGHT_CLAUDE,
        "OpenAI":  WEIGHT_OPENAI,
        "Gemini":  WEIGHT_GEMINI,
        "Mistral": WEIGHT_MISTRAL,
    }

    scores_por_ia = {r.ia_nombre: r.score for r in resultados}

    score_ponderado = 0.0
    peso_total = 0.0

    for resultado in resultados:
        peso = pesos.get(resultado.ia_nombre, 0)
        score_ponderado += resultado.score * peso
        peso_total += peso

    score_final = round(score_ponderado / peso_total if peso_total > 0 else 0, 1)

    scores = list(scores_por_ia.values())
    promedio = sum(scores) / len(scores)
    varianza = round(sum((s - promedio) ** 2 for s in scores) / len(scores), 2)

    if varianza <= 25:
        nivel_acuerdo = "Alto"     
    elif varianza <= 100:
        nivel_acuerdo = "Medio"    
    else:
        nivel_acuerdo = "Bajo"  

    ia_mas_alta = max(scores_por_ia, key=scores_por_ia.get)
    ia_mas_baja = min(scores_por_ia, key=scores_por_ia.get)

    return {
        "score_final":   score_final,
        "scores_por_ia": scores_por_ia,
        "nivel_acuerdo": nivel_acuerdo,
        "varianza":      varianza,
        "ia_mas_alta":   ia_mas_alta,
        "ia_mas_baja":   ia_mas_baja,
    }
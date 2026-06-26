from src.analyzers.providers.base_analyzer import ResultadoAnalisis
from config.settings import WEIGHT_OPENAI, WEIGHT_MISTRAL


def calcular_score_consenso(resultados: list[ResultadoAnalisis]) -> dict:
    if not resultados:
        raise ValueError("No hay resultados para calcular el score")

    pesos = {
        "OpenAI":  WEIGHT_OPENAI,
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
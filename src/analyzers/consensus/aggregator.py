from src.analyzers.providers.base_analyzer import ResultadoAnalisis
from config.settings import WEIGHT_OPENAI, WEIGHT_MISTRAL


def agregar_resultados(resultados: list[ResultadoAnalisis]) -> dict:
    if not resultados:
        raise ValueError("No hay resultados de IAs para agregar")

    pesos = {
        "OpenAI":  WEIGHT_OPENAI,
        "Mistral": WEIGHT_MISTRAL,
    }

    score_final = 0.0
    peso_total = 0.0

    for resultado in resultados:
        peso = pesos.get(resultado.ia_nombre, 0)
        score_final += resultado.score * peso
        peso_total += peso

    if peso_total > 0:
        score_final = score_final / peso_total

    skills_union = list(set(
        skill
        for resultado in resultados
        for skill in resultado.skills
    ))

    experiencia_consolidada = _consolidar_experiencia(resultados)
    fortalezas_consenso = _encontrar_consenso([r.fortalezas for r in resultados])
    debilidades_consenso = _encontrar_consenso([r.debilidades for r in resultados])

    niveles = [r.nivel for r in resultados]
    nivel_final = max(set(niveles), key=niveles.count)

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
    mejor = max(resultados, key=lambda r: r.score)
    return mejor.experiencia


def _encontrar_consenso(listas: list[list[str]], min_coincidencias: int = 2) -> list[str]:
    conteo = {}
    for lista in listas:
        for item in lista:
            conteo[item] = conteo.get(item, 0) + 1

    consenso = [item for item, cnt in conteo.items() if cnt >= min_coincidencias]
    return consenso if consenso else list(conteo.keys())
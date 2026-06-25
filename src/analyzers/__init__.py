from src.analyzers.providers import ClaudeAnalyzer, OpenAIAnalyzer, GeminiAnalyzer, MistralAnalyzer
from src.analyzers.consensus import agregar_resultados, calcular_score_consenso


def analizar_cv(cv_texto: str, oferta_trabajo: str = None) -> dict:
    """
    Corre el análisis con todas las IAs y retorna el consenso final.
    Punto de entrada principal para analizar un CV.
    """
    analizadores = [
        ClaudeAnalyzer(),
        OpenAIAnalyzer(),
        GeminiAnalyzer(),
        MistralAnalyzer(),
    ]

    resultados = []
    for analizador in analizadores:
        try:
            resultado = analizador.analizar(cv_texto, oferta_trabajo)
            resultados.append(resultado)
        except Exception as e:
            print(f"Error con {analizador.__class__.__name__}: {e}")

    consenso = agregar_resultados(resultados)
    scoring  = calcular_score_consenso(resultados)

    return {**consenso, **scoring}
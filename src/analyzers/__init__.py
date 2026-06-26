from src.analyzers.providers import OpenAIAnalyzer, MistralAnalyzer
from src.analyzers.consensus import agregar_resultados, calcular_score_consenso
import streamlit as st


def analizar_cv(cv_texto: str, oferta_trabajo: str = None) -> dict:
    analizadores = [
        OpenAIAnalyzer(),
        MistralAnalyzer(),
    ]

    resultados = []
    for analizador in analizadores:
        try:
            resultado = analizador.analizar(cv_texto, oferta_trabajo)
            resultados.append(resultado)
        except Exception as e:
            st.error(f"Error con {analizador.__class__.__name__}: {e}")

    consenso = agregar_resultados(resultados)
    scoring  = calcular_score_consenso(resultados)

    return {**consenso, **scoring}
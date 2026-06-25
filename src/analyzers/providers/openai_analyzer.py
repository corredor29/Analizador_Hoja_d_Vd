import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.analyzers.providers.base_analyzer import BaseAnalyzer, ResultadoAnalisis
from config.settings import OPENAI_API_KEY, MAX_TOKENS


class OpenAIAnalyzer(BaseAnalyzer):

    def __init__(self):
        self.cliente = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o",
            max_tokens=MAX_TOKENS,
        )

    def analizar(self, cv_texto: str, oferta_trabajo: str = None) -> ResultadoAnalisis:
        prompt = self._construir_prompt(cv_texto, oferta_trabajo)
        respuesta = self.cliente.invoke([HumanMessage(content=prompt)])
        datos = json.loads(respuesta.content)

        return ResultadoAnalisis(
            ia_nombre="OpenAI",
            score=datos["score"],
            skills=datos["skills"],
            experiencia=datos["experiencia"],
            fortalezas=datos["fortalezas"],
            debilidades=datos["debilidades"],
            recomendaciones=datos["recomendaciones"],
            nivel=datos["nivel"],
            resumen=datos["resumen"],
        )
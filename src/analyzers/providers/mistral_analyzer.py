import json
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from src.analyzers.providers.base_analyzer import BaseAnalyzer, ResultadoAnalisis
from config.settings import MISTRAL_API_KEY, MAX_TOKENS


class MistralAnalyzer(BaseAnalyzer):

    def __init__(self):
        self.cliente = ChatMistralAI(
            api_key=MISTRAL_API_KEY,
            model="mistral-large-latest",
            max_tokens=MAX_TOKENS,
        )

    def analizar(self, cv_texto: str, oferta_trabajo: str = None) -> ResultadoAnalisis:
        prompt = self._construir_prompt(cv_texto, oferta_trabajo)
        respuesta = self.cliente.invoke([HumanMessage(content=prompt)])
        datos = json.loads(respuesta.content)

        return ResultadoAnalisis(
            ia_nombre="Mistral",
            score=datos["score"],
            skills=datos["skills"],
            experiencia=datos["experiencia"],
            fortalezas=datos["fortalezas"],
            debilidades=datos["debilidades"],
            recomendaciones=datos["recomendaciones"],
            nivel=datos["nivel"],
            resumen=datos["resumen"],
        )
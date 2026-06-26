import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ResultadoAnalisis:
    """Estructura estándar que debe retornar cada IA."""
    ia_nombre: str
    score: float
    skills: list[str]
    experiencia: list[dict]
    fortalezas: list[str]
    debilidades: list[str]
    recomendaciones: list[str]
    nivel: str
    resumen: str


class BaseAnalyzer(ABC):
    """
    Clase base que deben implementar todos los analizadores de IA.
    Garantiza que OpenAI, Gemini y Mistral retornen la misma estructura.
    """

    @abstractmethod
    def analizar(self, cv_texto: str, oferta_trabajo: str = None) -> ResultadoAnalisis:
        pass

    def _extraer_json(self, contenido: str) -> dict:
        contenido = contenido.strip()
        try:
            return json.loads(contenido)
        except json.JSONDecodeError:
            pass
        match = re.search(r'\{.*\}', contenido, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"No se encontró JSON válido en la respuesta: {contenido[:300]!r}")

    def _construir_prompt(self, cv_texto: str, oferta_trabajo: str = None) -> str:
        prompt = f"""
Eres un analizador de hojas de vida. Analiza el siguiente CV y responde ÚNICAMENTE con un objeto JSON válido.
No incluyas texto adicional, no uses markdown, no uses bloques de código, no des explicaciones.
Responde solo con el JSON puro, comenzando con {{ y terminando con }}.

El JSON debe tener exactamente esta estructura:
{{
    "score": 75,
    "skills": ["Python", "SQL"],
    "experiencia": [
        {{"cargo": "Desarrollador", "empresa": "Empresa S.A.", "años": 2}}
    ],
    "fortalezas": ["Buena experiencia técnica"],
    "debilidades": ["Poca experiencia en cloud"],
    "recomendaciones": ["Certificarse en AWS"],
    "nivel": "Junior",
    "resumen": "Candidato con perfil técnico sólido."
}}

Los valores del campo nivel solo pueden ser: "Junior", "Mid" o "Senior".
El campo score debe ser un número entre 0 y 100.

CV A ANALIZAR:
{cv_texto}
"""
        if oferta_trabajo:
            prompt += f"""
OFERTA DE TRABAJO (considera este contexto para el score y análisis):
{oferta_trabajo}
"""
        return prompt
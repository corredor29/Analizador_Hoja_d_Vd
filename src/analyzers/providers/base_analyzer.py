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
    Garantiza que Claude, OpenAI y Gemini retornen la misma estructura.
    """

    @abstractmethod
    def analizar(self, cv_texto: str, oferta_trabajo: str = None) -> ResultadoAnalisis:
        """
        Analiza el texto de un CV y retorna un ResultadoAnalisis.
        
        Args:
            cv_texto: Texto extraído del CV
            oferta_trabajo: Descripción del cargo (opcional, para job matching)
        
        Returns:
            ResultadoAnalisis con score, skills, experiencia, etc.
        """
        pass

    def _construir_prompt(self, cv_texto: str, oferta_trabajo: str = None) -> str:
        """Prompt base compartido por todas las IAs."""
        prompt = f"""
Analiza el siguiente CV y responde ÚNICAMENTE en formato JSON con esta estructura exacta:
{{
    "score": <número del 0 al 100>,
    "skills": ["skill1", "skill2", ...],
    "experiencia": [
        {{"cargo": "...", "empresa": "...", "años": <número>}}
    ],
    "fortalezas": ["fortaleza1", "fortaleza2", ...],
    "debilidades": ["debilidad1", "debilidad2", ...],
    "recomendaciones": ["recomendacion1", ...],
    "nivel": "Junior" | "Mid" | "Senior",
    "resumen": "Resumen general del candidato en 2-3 oraciones"
}}

CV A ANALIZAR:
{cv_texto}
"""
        if oferta_trabajo:
            prompt += f"""
OFERTA DE TRABAJO (considera este contexto para el score y análisis):
{oferta_trabajo}
"""
        return prompt
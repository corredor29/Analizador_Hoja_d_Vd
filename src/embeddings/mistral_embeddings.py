import numpy as np
from langchain_mistralai import MistralAIEmbeddings
from config.settings import MISTRAL_API_KEY

_embedder = None


def _get_embedder() -> MistralAIEmbeddings:
    global _embedder
    if _embedder is None:
        _embedder = MistralAIEmbeddings(
            api_key=MISTRAL_API_KEY,
            model="mistral-embed",
        )
    return _embedder


def obtener_embedding(texto: str) -> list[float]:
    """Retorna el vector embedding de un texto usando Mistral."""
    return _get_embedder().embed_query(texto)


def calcular_similitud_semantica(texto1: str, texto2: str) -> float:
    """
    Calcula la similitud coseno entre dos textos usando embeddings de Mistral.
    Retorna un valor entre 0 y 1 (1 = idénticos semánticamente).
    """
    embedder = _get_embedder()
    vectores = embedder.embed_documents([texto1, texto2])
    a = np.array(vectores[0])
    b = np.array(vectores[1])
    norma = np.linalg.norm(a) * np.linalg.norm(b)
    if norma == 0:
        return 0.0
    return float(np.dot(a, b) / norma)

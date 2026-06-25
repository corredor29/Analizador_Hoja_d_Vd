from sqlalchemy.orm import Session
from sqlalchemy import select
from pgvector.sqlalchemy import Vector
from database.models import Analisis


def crear_analisis(
    session: Session,
    candidato_id: int,
    skills: list,
    experiencia: list,
    score_claude: float,
    score_openai: float,
    score_gemini: float,
    score_final: float,
    embedding: list[float] | None = None,
) -> Analisis:
    """Guarda el resultado del análisis multi-IA de un CV."""
    analisis = Analisis(
        candidato_id=candidato_id,
        skills=skills,
        experiencia=experiencia,
        score_claude=score_claude,
        score_openai=score_openai,
        score_gemini=score_gemini,
        score_final=score_final,
        embedding=embedding,
    )
    session.add(analisis)
    session.commit()
    session.refresh(analisis)
    return analisis


def obtener_por_candidato(session: Session, candidato_id: int) -> list[Analisis]:
    """Retorna todos los análisis de un candidato ordenados por fecha."""
    return (
        session.query(Analisis)
        .filter(Analisis.candidato_id == candidato_id)
        .order_by(Analisis.created_at.desc())
        .all()
    )


def obtener_ultimo_analisis(session: Session, candidato_id: int) -> Analisis | None:
    """Retorna el análisis más reciente de un candidato."""
    return (
        session.query(Analisis)
        .filter(Analisis.candidato_id == candidato_id)
        .order_by(Analisis.created_at.desc())
        .first()
    )


def buscar_similares(
    session: Session, embedding: list[float], limite: int = 5
) -> list[Analisis]:
    """
    Busca los CVs más similares usando pgvector.
    Retorna los 'limite' análisis más cercanos al embedding dado.
    """
    return (
        session.query(Analisis)
        .filter(Analisis.embedding.isnot(None))
        .order_by(Analisis.embedding.l2_distance(embedding))
        .limit(limite)
        .all()
    )


def listar_todos(session: Session) -> list[Analisis]:
    """Retorna todos los análisis ordenados por score final."""
    return session.query(Analisis).order_by(Analisis.score_final.desc()).all()
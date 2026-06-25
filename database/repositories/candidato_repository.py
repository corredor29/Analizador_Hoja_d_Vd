from sqlalchemy.orm import Session
from database.models import Candidato


def crear_candidato(session: Session, nombre: str, email: str) -> Candidato:
    """Crea un candidato nuevo. Si el email ya existe lo retorna sin duplicar."""
    existente = obtener_por_email(session, email)
    if existente:
        return existente

    candidato = Candidato(nombre=nombre, email=email)
    session.add(candidato)
    session.commit()
    session.refresh(candidato)
    return candidato


def obtener_por_email(session: Session, email: str) -> Candidato | None:
    """Busca un candidato por email."""
    return session.query(Candidato).filter(Candidato.email == email).first()


def obtener_por_id(session: Session, candidato_id: int) -> Candidato | None:
    """Busca un candidato por ID."""
    return session.query(Candidato).filter(Candidato.id == candidato_id).first()


def listar_candidatos(session: Session) -> list[Candidato]:
    """Retorna todos los candidatos ordenados por fecha de creación."""
    return session.query(Candidato).order_by(Candidato.created_at.desc()).all()


def eliminar_candidato(session: Session, candidato_id: int) -> bool:
    """Elimina un candidato y todos sus análisis (cascade)."""
    candidato = obtener_por_id(session, candidato_id)
    if not candidato:
        return False

    session.delete(candidato)
    session.commit()
    return True
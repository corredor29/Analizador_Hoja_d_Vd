from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Candidato(Base):
    """Datos básicos del candidato extraídos del CV."""
    __tablename__ = "candidatos"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    nombre   = Column(String(150), nullable=False)
    email    = Column(String(150), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analisis = relationship("Analisis", back_populates="candidato")

    def __repr__(self):
        return f"<Candidato {self.nombre} - {self.email}>"


class Analisis(Base):
    """Resultado del análisis multi-IA de un CV."""
    __tablename__ = "analisis"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    skills      = Column(JSON, nullable=True)  
    experiencia = Column(JSON, nullable=True) 

    score_claude = Column(Float, nullable=True)
    score_openai = Column(Float, nullable=True)
    score_gemini = Column(Float, nullable=True)

    score_final  = Column(Float, nullable=False)

    embedding = Column(Vector(1536), nullable=True) 

    candidato = relationship("Candidato", back_populates="analisis")

    def __repr__(self):
        return f"<Analisis candidato_id={self.candidato_id} score={self.score_final}>"
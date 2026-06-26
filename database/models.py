from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Candidato(Base):
    __tablename__ = "candidatos"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    nombre     = Column(String(150), nullable=False)
    email      = Column(String(150), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analisis = relationship("Analisis", back_populates="candidato")


class Analisis(Base):
    __tablename__ = "analisis"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(Integer, ForeignKey("candidatos.id"), nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)

    skills      = Column(JSON, nullable=True)
    experiencia = Column(JSON, nullable=True)

    score_openai = Column(Float, nullable=True)
    score_gemini = Column(Float, nullable=True)
    score_mistral = Column(Float, nullable=True)
    score_final  = Column(Float, nullable=False)

    candidato = relationship("Candidato", back_populates="analisis")
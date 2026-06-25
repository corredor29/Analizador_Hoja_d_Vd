from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base
from config.settings import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Session:
    """Retorna una sesión de base de datos."""
    return SessionLocal()


def init_db():
    """
    Crea las tablas en PostgreSQL si no existen.
    También activa la extensión pgvector.
    Llamar una sola vez al iniciar la app.
    """
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(bind=engine)


def check_connection() -> bool:
    """Verifica que la conexión a PostgreSQL esté activa."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
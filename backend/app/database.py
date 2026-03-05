from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

Base = declarative_base()

_engine = None

def _build_engine():
    settings = get_settings()
    url = settings.DATABASE_URL
    # Railway provides postgres:// but SQLAlchemy 2.x requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return create_engine(url, pool_pre_ping=True, pool_size=10, max_overflow=20)

def get_engine():
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine

def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

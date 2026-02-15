from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# For SQLite, we need to disable same_thread_check for multithreaded apps (like FastAPI)
# When moving to Postgres, remove connect_args={"check_same_thread": False}
connect_args = (
    {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

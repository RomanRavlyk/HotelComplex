from sqlmodel import create_engine, Session, SQLModel
from .config import settings

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
from sqlmodel import create_engine, Session, SQLModel
import os
from pydantic_settings import BaseSettings
from app.Hotel.models import HotelDB
from app.Cottage.models import CottageDB
from app.Amenity.models import HotelAmenityDB, CottageAmenityDB

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = '.env'

settings = Settings()

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
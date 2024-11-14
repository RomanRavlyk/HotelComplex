import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get('DATABASE_URL')

    class Config:
        env_file = '.env'

settings = Settings()
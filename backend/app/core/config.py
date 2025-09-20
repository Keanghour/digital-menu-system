# app/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project Info
    APP_NAME: str = "FastAPI Project"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # JWT / Security
    SECRET_KEY: str
    # ALGORITHM: str = "RS256"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

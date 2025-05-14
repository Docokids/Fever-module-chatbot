# src/core/config.py
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DocoChat API"
    llm_provider: str = "gemini"  # Por defecto usamos Gemini
    gemini_api_key: str
    redis_url: str = "redis://localhost:6379"
    postgres_url: str = "postgresql+asyncpg://user:password@localhost:5432/docochat"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

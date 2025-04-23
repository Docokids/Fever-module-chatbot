# src/core/config.py
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str
    llm_provider: str
    openai_api_key: str
    redis_url: str
    postgres_url: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# src/core/config.py
from functools import lru_cache
import os
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    # App settings
    app_name: str = "DocoChat API"
    debug: bool = False
    
    # LLM Provider settings
    llm_provider: Literal["gemini", "openai"] = "gemini"  # Por defecto usamos Gemini
    # obtener de la variable de entorno
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    openai_api_key: Optional[str] = None
    
    # Database settings
    redis_url: str = "redis://redis:6379/0"
    postgres_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/docochat"
    
    # Optional settings
    sentry_dsn: Optional[str] = None
    prometheus_port: int = 9090

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        validate_default=True,
        str_strip_whitespace=True,
        env_prefix="",  # No prefix for environment variables
        use_enum_values=True
    )

    @field_validator("llm_provider")
    @classmethod
    def validate_llm_provider(cls, v):
        if v not in ["gemini", "openai"]:
            raise ValueError("Invalid LLM provider")
        return v

@lru_cache()
def get_settings() -> Settings:
    return Settings()

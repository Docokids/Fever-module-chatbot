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
    llm_provider: Literal["gemini", "openai", "deepseek", "local"] = "gemini"  # Por defecto usamos Gemini
    
    # API Keys
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    
    # Model configurations
    llm_model: str = "gemini-2.0-flash"  # Modelo por defecto
    llm_temperature: float = 0.7
    llm_max_tokens: Optional[int] = None
    
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
        valid_providers = ["gemini", "openai", "deepseek", "local"]
        if v not in valid_providers:
            raise ValueError(f"Invalid LLM provider. Must be one of: {valid_providers}")
        return v
    
    @field_validator("llm_temperature")
    @classmethod
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v
    
    def get_required_api_key(self) -> Optional[str]:
        """Retorna la API key requerida para el proveedor configurado."""
        api_key_map = {
            "gemini": self.gemini_api_key,
            "openai": self.openai_api_key,
            "deepseek": self.deepseek_api_key,
            "local": None  # Local no requiere API key
        }
        return api_key_map.get(self.llm_provider)
    
    def validate_provider_config(self) -> bool:
        """Valida que la configuración del proveedor sea correcta."""
        if self.llm_provider == "local":
            return True  # Local no requiere validación de API key
        
        api_key = self.get_required_api_key()
        if not api_key:
            raise ValueError(f"API key required for provider: {self.llm_provider}")
        
        return True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

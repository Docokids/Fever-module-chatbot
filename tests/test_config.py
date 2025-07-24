import pytest
import os
from src.core.config import Settings, get_settings

def test_default_settings():
    # Test configuración por defecto
    settings = Settings()
    assert settings.app_name == "DocoChat API"
    assert settings.llm_provider == "gemini"
    assert settings.redis_url == "redis://redis:6379/0"
    assert settings.postgres_url == "postgresql+asyncpg://postgres:postgres@db:5432/docochat"

def test_settings_validation():
    # Test validation of LLM provider
    with pytest.raises(ValueError, match="Input should be"):
        Settings(llm_provider="invalid_provider", _env_file=None, _env_prefix="")
    
    # Test valid providers
    settings = Settings(llm_provider="gemini", _env_file=None, _env_prefix="")
    assert settings.llm_provider == "gemini"
    
    settings = Settings(llm_provider="openai", _env_file=None, _env_prefix="")
    assert settings.llm_provider == "openai"

def test_get_settings_caching():
    # Test que get_settings usa caché
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2  # Debe ser la misma instancia 
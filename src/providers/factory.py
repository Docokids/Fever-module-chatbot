# src/providers/factory.py
from src.core.config import get_settings
from src.providers.gemini_client import GeminiClient
from src.providers.interface import LLMClient

def get_llm_client() -> LLMClient:
    settings = get_settings()
    
    if settings.llm_provider == "gemini":
        return GeminiClient()
    else:
        raise ValueError(f"Proveedor LLM no soportado: {settings.llm_provider}")

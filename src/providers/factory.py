# src/providers/factory.py
from src.core.config import Settings
from src.providers.gemini_client import GeminiClient
from src.providers.interface import LLMClient

def get_llm_client(settings: Settings | None = None) -> LLMClient:
    """
    Obtiene el cliente LLM configurado según el proveedor especificado.
    
    Args:
        settings (Settings | None): Configuración de la aplicación. Si es None, se usará la configuración por defecto.
        
    Returns:
        LLMClient: Cliente LLM configurado
        
    Raises:
        ValueError: Si el proveedor LLM no es válido
    """
    if not settings:
        settings = Settings()
        
    if settings.llm_provider == "gemini":
        return GeminiClient(settings)
    else:
        raise ValueError(f"Proveedor LLM no soportado: {settings.llm_provider}")

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from src.core.config import Settings

def get_llm_client(settings: Settings) -> BaseChatModel:
    """
    Obtiene el cliente LLM configurado según el proveedor especificado.
    
    Args:
        settings (Settings): Configuración de la aplicación
        
    Returns:
        BaseChatModel: Cliente LLM configurado
        
    Raises:
        ValueError: Si el proveedor LLM no es válido
    """
    if settings.llm_provider == "openai":
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key
        )
    elif settings.llm_provider == "anthropic":
        return ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.anthropic_api_key
        )
    else:
        raise ValueError(f"Proveedor LLM no válido: {settings.llm_provider}") 
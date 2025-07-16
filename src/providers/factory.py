# src/providers/factory.py
from typing import Dict, Type
from src.core.config import Settings
from src.providers.interface import LLMClient
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.providers.adapters.gemini_adapter import GeminiAdapter
from src.providers.adapters.openai_adapter import OpenAIAdapter
from src.providers.adapters.deepseek_adapter import DeepSeekAdapter
from src.providers.adapters.local_adapter import LocalAdapter
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    Factory mejorado para crear clientes LLM con soporte para múltiples proveedores.
    Implementa registro dinámico de adapters y validación de configuración.
    """
    
    def __init__(self):
        self._adapters: Dict[str, Type[BaseLLMAdapter]] = {}
        self._register_default_adapters()
    
    def _register_default_adapters(self):
        """Registra los adapters por defecto."""
        self.register_adapter("gemini", GeminiAdapter)
        self.register_adapter("openai", OpenAIAdapter)
        self.register_adapter("deepseek", DeepSeekAdapter)
        self.register_adapter("local", LocalAdapter)
    
    def register_adapter(self, provider_name: str, adapter_class: Type[BaseLLMAdapter]):
        """
        Registra un nuevo adapter para un proveedor.
        
        Args:
            provider_name: Nombre del proveedor (ej: "gemini", "openai")
            adapter_class: Clase del adapter que extiende BaseLLMAdapter
        """
        self._adapters[provider_name] = adapter_class
        logger.info(f"Registered adapter for provider: {provider_name}")
    
    def get_available_providers(self) -> list:
        """Retorna la lista de proveedores disponibles."""
        return list(self._adapters.keys())
    
    def create_adapter(self, provider_name: str, settings: Settings | None = None) -> BaseLLMAdapter:
        """
        Crea una instancia del adapter para el proveedor especificado.
        
        Args:
            provider_name: Nombre del proveedor
            settings: Configuración de la aplicación
            
        Returns:
            Instancia del adapter configurado
            
        Raises:
            ValueError: Si el proveedor no está registrado o la configuración es inválida
        """
        if provider_name not in self._adapters:
            available = ", ".join(self.get_available_providers())
            raise ValueError(f"Proveedor LLM no soportado: {provider_name}. Proveedores disponibles: {available}")
        
        adapter_class = self._adapters[provider_name]
        
        try:
            # Validar configuración del proveedor
            if settings:
                settings.validate_provider_config()
            
            adapter = adapter_class(settings)
            logger.info(f"Successfully created adapter for provider: {provider_name}")
            return adapter
        except Exception as e:
            logger.error(f"Error creating adapter for provider {provider_name}: {str(e)}")
            raise ValueError(f"Error initializing {provider_name} adapter: {str(e)}")

# Instancia global del factory
_llm_factory = LLMFactory()

def get_llm_client(settings: Settings | None = None) -> LLMClient:
    """
    Obtiene el cliente LLM configurado según el proveedor especificado.
    
    Args:
        settings (Settings | None): Configuración de la aplicación. Si es None, se usará la configuración por defecto.
        
    Returns:
        LLMClient: Cliente LLM configurado
        
    Raises:
        ValueError: Si el proveedor LLM no es válido o no se puede inicializar
    """
    if not settings:
        settings = Settings()
    
    provider_name = settings.llm_provider
    logger.info(f"Creating LLM client for provider: {provider_name}")
    
    return _llm_factory.create_adapter(provider_name, settings)

def register_provider(provider_name: str, adapter_class: Type[BaseLLMAdapter]):
    """
    Registra un nuevo proveedor LLM.
    
    Args:
        provider_name: Nombre del proveedor
        adapter_class: Clase del adapter que extiende BaseLLMAdapter
    """
    _llm_factory.register_adapter(provider_name, adapter_class)

def get_available_providers() -> list:
    """Retorna la lista de proveedores disponibles."""
    return _llm_factory.get_available_providers()

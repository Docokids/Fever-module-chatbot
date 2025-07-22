# src/providers/factory.py
from src.core.config import Settings
from src.providers.interface import LLMClient
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    """
    Factory mejorado para crear clientes LLM con soporte para múltiples proveedores.
    Implementa registro dinámico de adapters y validación de configuración.
    """
    def __init__(self):
        self._adapters = {}
        self._register_default_adapters()

    def _register_default_adapters(self):
        self.register_adapter("gemini", self._import_gemini)
        self.register_adapter("openai", self._import_openai)
        self.register_adapter("deepseek", self._import_deepseek)
        self.register_adapter("local", self._import_local)

    def register_adapter(self, provider_name, import_func):
        self._adapters[provider_name] = import_func
        logger.info(f"Registered adapter for provider: {provider_name}")

    def get_available_providers(self):
        return list(self._adapters.keys())

    def create_adapter(self, provider_name: str, settings: Settings | None = None) -> LLMClient:
        if provider_name not in self._adapters:
            available = ", ".join(self.get_available_providers())
            raise ValueError(f"Proveedor LLM no soportado: {provider_name}. Proveedores disponibles: {available}")
        try:
            # Validar configuración del proveedor
            if settings:
                settings.validate_provider_config()
            AdapterClass = self._adapters[provider_name]()
            adapter = AdapterClass(settings)
            logger.info(f"Successfully created adapter for provider: {provider_name}")
            return adapter
        except ImportError as e:
            logger.error(f"No se pudo importar el adapter para {provider_name}: {e}")
            raise ImportError(f"Dependencias faltantes para el proveedor {provider_name}. Instala el requirements correspondiente.")
        except Exception as e:
            logger.error(f"Error creating adapter for provider {provider_name}: {str(e)}")
            raise ValueError(f"Error initializing {provider_name} adapter: {str(e)}")

    def _import_gemini(self):
        from src.providers.adapters.gemini_adapter import GeminiAdapter
        return GeminiAdapter

    def _import_openai(self):
        from src.providers.adapters.openai_adapter import OpenAIAdapter
        return OpenAIAdapter

    def _import_deepseek(self):
        from src.providers.adapters.deepseek_adapter import DeepSeekAdapter
        return DeepSeekAdapter

    def _import_local(self):
        from src.providers.adapters.local_adapter import LocalAdapter
        return LocalAdapter

# Instancia global del factory
_llm_factory = LLMFactory()

def get_llm_client(settings: Settings | None = None) -> LLMClient:
    if not settings:
        settings = Settings()
    provider_name = settings.llm_provider
    logger.info(f"Creating LLM client for provider: {provider_name}")
    return _llm_factory.create_adapter(provider_name, settings)

def register_provider(provider_name: str, import_func):
    _llm_factory.register_adapter(provider_name, import_func)

def get_available_providers() -> list:
    return _llm_factory.get_available_providers()

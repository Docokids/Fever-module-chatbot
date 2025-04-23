# src/providers/factory.py
from src.providers.interface import LLMClient
from src.providers.openai_client import OpenAIClient
# from src.providers.gemini_client import GeminiClient
from src.providers.local_client import LocalLLMClient

def get_llm_client(settings) -> LLMClient:
    if settings.llm_provider == "openai":
        return OpenAIClient(api_key=settings.openai_api_key)
    if settings.llm_provider == "gemini":
        return GeminiClient(...)
    return LocalLLMClient(model_path="...")

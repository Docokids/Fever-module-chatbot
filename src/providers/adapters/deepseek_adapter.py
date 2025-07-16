# src/providers/adapters/deepseek_adapter.py
import requests
from typing import List, Any, Dict
from src.models.schemas import Message
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.core.config import get_settings, Settings
import logging
import json

logger = logging.getLogger(__name__)

class DeepSeekAdapter(BaseLLMAdapter):
    """
    Adapter específico para DeepSeek.
    Implementa la interfaz específica de DeepSeek para la generación de respuestas.
    """
    
    def __init__(self, settings: Settings | None = None):
        super().__init__(settings or get_settings())
        self._initialize_deepseek()
    
    def _initialize_deepseek(self):
        """Inicializa el cliente de DeepSeek."""
        self.logger.info(f"Initializing DeepSeekAdapter with settings: {self.settings}")
        self.logger.info(f"DeepSeek API Key present: {'Yes' if self.settings.deepseek_api_key else 'No'}")
        
        if not self.settings.deepseek_api_key:
            self.logger.error("DeepSeek API key is missing")
            raise ValueError("DeepSeek API key is required. Please set DEEPSEEK_API_KEY environment variable.")
        
        try:
            self.api_key = self.settings.deepseek_api_key
            self.base_url = "https://api.deepseek.com/v1/chat/completions"
            self.model = self.settings.llm_model or "deepseek-chat"
            self.logger.info(f"DeepSeek client initialized successfully with model: {self.model}")
        except Exception as e:
            self.logger.error(f"Error initializing DeepSeek client: {str(e)}")
            raise
    
    def _format_messages_for_provider(self, context: List[Message], system_prompt: str) -> List[Dict[str, str]]:
        """
        Formatea los mensajes para el formato específico de DeepSeek.
        
        Args:
            context: Lista de mensajes de la conversación
            system_prompt: Prompt del sistema
            
        Returns:
            Lista de mensajes formateados para DeepSeek
        """
        # Crear el mensaje del sistema
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Agregar el historial de la conversación
        for msg in context:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return messages
    
    async def _call_provider(self, formatted_messages: List[Dict[str, str]]) -> str:
        """
        Llama al modelo de DeepSeek para generar la respuesta.
        
        Args:
            formatted_messages: Mensajes formateados para DeepSeek
            
        Returns:
            Texto de la respuesta generada
        """
        try:
            # Configurar parámetros de generación
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": self.settings.llm_temperature,
                "max_tokens": self.settings.llm_max_tokens or 1000,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Realizar la petición HTTP
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Verificar si la petición fue exitosa
            response.raise_for_status()
            
            # Parsear la respuesta
            response_data = response.json()
            response_text = response_data["choices"][0]["message"]["content"]
            
            self.logger.info(f"DeepSeek response generated: {response_text[:100]}...")
            
            return response_text
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling DeepSeek provider (HTTP error): {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error calling DeepSeek provider: {str(e)}")
            raise 
# src/providers/adapters/openai_adapter.py
import openai
from typing import List, Any, Dict
from src.models.schemas import Message
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.core.config import get_settings, Settings
import logging

logger = logging.getLogger(__name__)

class OpenAIAdapter(BaseLLMAdapter):
    """
    Adapter específico para OpenAI.
    Implementa la interfaz específica de OpenAI para la generación de respuestas.
    """
    
    def __init__(self, settings: Settings | None = None):
        super().__init__(settings or get_settings())
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Inicializa el cliente de OpenAI."""
        self.logger.info(f"Initializing OpenAIAdapter with settings: {self.settings}")
        self.logger.info(f"OpenAI API Key present: {'Yes' if self.settings.openai_api_key else 'No'}")
        
        if not self.settings.openai_api_key:
            self.logger.error("OpenAI API key is missing")
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable.")
        
        try:
            openai.api_key = self.settings.openai_api_key
            self.model = self.settings.llm_model or "gpt-4o-mini"
            self.logger.info(f"OpenAI client initialized successfully with model: {self.model}")
        except Exception as e:
            self.logger.error(f"Error initializing OpenAI client: {str(e)}")
            raise
    
    def _format_messages_for_provider(self, context: List[Message], system_prompt: str) -> List[Dict[str, str]]:
        """
        Formatea los mensajes para el formato específico de OpenAI.
        
        Args:
            context: Lista de mensajes de la conversación
            system_prompt: Prompt del sistema
            
        Returns:
            Lista de mensajes formateados para OpenAI
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
        Llama al modelo de OpenAI para generar la respuesta.
        
        Args:
            formatted_messages: Mensajes formateados para OpenAI
            
        Returns:
            Texto de la respuesta generada
        """
        try:
            # Configurar parámetros de generación
            generation_params = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": self.settings.llm_temperature,
                "max_tokens": self.settings.llm_max_tokens or 1000
            }
            
            # Generar la respuesta usando el modelo
            response = openai.ChatCompletion.create(**generation_params)
            
            # Extraer el texto de la respuesta
            response_text = response.choices[0].message.content
            
            self.logger.info(f"OpenAI response generated: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error calling OpenAI provider: {str(e)}")
            raise 
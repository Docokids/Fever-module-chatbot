# src/providers/adapters/gemini_adapter.py
import google.generativeai as genai
from typing import List, Any, Dict
from src.models.schemas import Message
from src.providers.adapters.base_adapter import BaseLLMAdapter
from src.core.config import get_settings, Settings
import logging

logger = logging.getLogger(__name__)

class GeminiAdapter(BaseLLMAdapter):
    """
    Adapter específico para Google Gemini.
    Implementa la interfaz específica de Gemini para la generación de respuestas.
    """
    
    def __init__(self, settings: Settings | None = None):
        super().__init__(settings or get_settings())
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Inicializa el cliente de Gemini."""
        self.logger.info(f"Initializing GeminiAdapter with settings: {self.settings}")
        self.logger.info(f"Gemini API Key present: {'Yes' if self.settings.gemini_api_key else 'No'}")
        
        if not self.settings.gemini_api_key:
            self.logger.error("Gemini API key is missing")
            raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY environment variable.")
        
        try:
            genai.configure(api_key=self.settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.logger.info("Gemini client initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing Gemini client: {str(e)}")
            raise
    
    def _format_messages_for_provider(self, context: List[Message], system_prompt: str) -> List[Dict[str, Any]]:
        """
        Formatea los mensajes para el formato específico de Gemini.
        
        Args:
            context: Lista de mensajes de la conversación
            system_prompt: Prompt del sistema
            
        Returns:
            Lista de mensajes formateados para Gemini
        """
        # Crear el mensaje del sistema
        system_message = {
            "role": "user",
            "parts": [system_prompt]
        }
        
        # Crear el historial de mensajes para Gemini
        messages = [system_message]
        
        # Agregar el historial de la conversación
        for msg in context:
            messages.append({
                "role": msg.role,
                "parts": [msg.content]
            })
        
        return messages
    
    async def _call_provider(self, formatted_messages: List[Dict[str, Any]]) -> str:
        """
        Llama al modelo de Gemini para generar la respuesta.
        
        Args:
            formatted_messages: Mensajes formateados para Gemini
            
        Returns:
            Texto de la respuesta generada
        """
        try:
            # Generar la respuesta usando el modelo
            response = self.model.generate_content(formatted_messages)
            
            # Extraer el texto de la respuesta
            response_text = response.text
            
            self.logger.info(f"Gemini response generated: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error calling Gemini provider: {str(e)}")
            raise 
import google.generativeai as genai
from typing import List
from src.models.schemas import Message
from src.providers.interface import LLMClient
from src.core.config import get_settings, Settings
import logging

logger = logging.getLogger(__name__)

class GeminiClient(LLMClient):
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        logger.info(f"Initializing GeminiClient with settings: {self.settings}")
        logger.info(f"Gemini API Key present: {'Yes' if self.settings.gemini_api_key else 'No'}")
        logger.info(f"API Key length: {len(self.settings.gemini_api_key) if self.settings.gemini_api_key else 0}")
        
        if not self.settings.gemini_api_key:
            logger.error("Gemini API key is missing")
            raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY environment variable or provide it in conversation settings.")
        
        try:
            genai.configure(api_key=self.settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.chat = self.model.start_chat(history=[])
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            raise

    async def generate(self, context: List[Message]) -> Message:
        try:
            # Convertir el contexto a formato que Gemini entienda
            for msg in context:
                if msg.role == "user":
                    self.chat.send_message(msg.content)
                elif msg.role == "assistant":
                    # Gemini maneja internamente el historial del asistente
                    pass

            # Obtener la última respuesta
            response = self.chat.last.text
            
            return Message(
                role="assistant",
                content=response
            )
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise 
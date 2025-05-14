import google.generativeai as genai
from typing import List
from src.models.schemas import Message
from src.providers.interface import LLMClient
from src.core.config import get_settings

class GeminiClient(LLMClient):
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])

    async def generate(self, context: List[Message]) -> Message:
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
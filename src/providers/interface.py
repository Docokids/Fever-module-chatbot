from abc import ABC, abstractmethod
from typing import List
from src.models.schemas import Message

class LLMClient(ABC):
    @abstractmethod
    async def generate(self, context: List[Message]) -> Message:
        """
        Genera una respuesta basada en el contexto de la conversación.
        
        Args:
            context: Lista de mensajes que forman el contexto de la conversación
            
        Returns:
            Message: La respuesta generada por el modelo
        """
        pass

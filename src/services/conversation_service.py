from uuid import UUID
from src.models.schemas import Conversation, Message, MessageCreate, MessageResponse, ConversationListItem
from src.db.repository import ConversationRepository
from src.providers.interface import LLMClient
from src.core.config import get_settings, Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.providers.factory import get_llm_client
from typing import List
import logging

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self, repo: ConversationRepository, llm: LLMClient | None = None):
        self.repo = repo
        self.llm = llm
        self.settings = get_settings()

    async def create_conversation(self, settings: Settings | None = None) -> Conversation:
        if settings:
            self.settings = settings
            # Reinicializar el cliente LLM con la nueva configuración
            self.llm = get_llm_client(settings)
        conv = Conversation()
        return await self.repo.create(conv)

    async def handle_message(self, conv_id: UUID, msg_in: MessageCreate) -> MessageResponse:
        # Recuperar historial
        conv = await self.repo.get(conv_id)
        if not conv:
            raise KeyError("Conversation not found")

        # Crear y guardar mensaje del usuario
        user_msg = Message(**msg_in.model_dump())
        conv.messages.append(user_msg)
        await self.repo.add_message(conv_id, user_msg)

        # Verificar si tenemos un cliente LLM
        if not self.llm:
            raise ValueError("LLM client not initialized. Please provide API key in conversation settings.")

        # Preparar el contexto para el LLM
        # Convertir todos los mensajes previos al formato que espera el LLM
        context_messages = []
        for msg in conv.messages:
            context_messages.append(Message(
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp
            ))

        logger.info(f"Enviando contexto con {len(context_messages)} mensajes al LLM")
        
        # Llamar al LLM con el contexto completo
        assistant_msg = await self.llm.generate(context_messages)
        
        # Guardar mensaje del asistente
        await self.repo.add_message(conv_id, assistant_msg)
        
        logger.info(f"Respuesta del LLM generada: {assistant_msg.content[:100]}...")
        
        return MessageResponse.model_validate(assistant_msg)

    async def get_conversation(self, conv_id: UUID) -> Conversation:
        conv = await self.repo.get(conv_id)
        if not conv:
            raise KeyError("Conversation not found")
        return conv

    async def list_conversations(self) -> List[ConversationListItem]:
        """Obtiene una lista de todas las conversaciones con información resumida"""
        conversations = await self.repo.list_all()
        result = []
        
        for conv in conversations:
            last_message = max(conv.messages, key=lambda x: x.timestamp) if conv.messages else None
            result.append(ConversationListItem(
                id=conv.id,
                message_count=len(conv.messages),
                last_message_timestamp=last_message.timestamp if last_message else None
            ))
        
        return result

# src/repositories/conversation_repository.py
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.schemas import Conversation, Message
from src.db.repository import ConversationRepository as BaseRepository

class ConversationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, conversation_id: UUID) -> Optional[Conversation]:
        """Obtiene una conversación por su ID"""
        query = select(Conversation).options(selectinload(Conversation.messages)).where(Conversation.id == conversation_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, conversation: Conversation) -> Conversation:
        """Crea una nueva conversación"""
        await self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def add_message(self, conversation_id: UUID, message: Message) -> Message:
        """Agrega un mensaje a una conversación existente"""
        conversation = await self.get(conversation_id)
        if not conversation:
            raise KeyError(f"Conversación {conversation_id} no encontrada")
        
        conversation.messages.append(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def list_all(self) -> List[Conversation]:
        """Lista todas las conversaciones"""
        query = select(Conversation).options(selectinload(Conversation.messages))
        result = await self.session.execute(query)
        return result.scalars().all() 
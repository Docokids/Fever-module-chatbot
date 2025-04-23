# src/db/repository.py
from abc import ABC, abstractmethod
from uuid import UUID
from src.models.schemas import Conversation

class ConversationRepository(ABC):
    @abstractmethod
    async def save(self, conv: Conversation) -> None: ...
    @abstractmethod
    async def get(self, conv_id: UUID) -> Conversation | None: ...

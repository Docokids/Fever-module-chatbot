# src/db/redis_repository.py
import json
from src.db.session import init_redis
from src.db.repository import ConversationRepository
from src.models.schemas import Conversation
from uuid import UUID

class RedisConversationRepository(ConversationRepository):
    def __init__(self, redis):
        self.redis = redis

    async def save(self, conv: Conversation) -> None:
        await self.redis.set(str(conv.id), conv.json())

    async def get(self, conv_id: UUID) -> Conversation | None:
        data = await self.redis.get(str(conv_id))
        return Conversation.parse_raw(data) if data else None

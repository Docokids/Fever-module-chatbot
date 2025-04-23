# src/db/postgres_repository.py
from src.db.repository import ConversationRepository
from src.db.session import AsyncSessionLocal
from src.models.schemas import Conversation
from uuid import UUID
from sqlalchemy import Table, Column, String, MetaData

# Supongamos una tabla sencilla de auditoría
metadata = MetaData()
conversations_table = Table(
    "conversations", metadata,
    Column("id", String, primary_key=True),
    Column("data", String)
)

class PostgresConversationRepository(ConversationRepository):
    async def save(self, conv: Conversation) -> None:
        async with AsyncSessionLocal() as session:
            await session.execute(
                conversations_table.insert().values(
                    id=str(conv.id),
                    data=conv.json()
                )
            )
            await session.commit()

    async def get(self, conv_id: UUID) -> Conversation | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                conversations_table.select().where(conversations_table.c.id == str(conv_id))
            )
            row = result.first()
            return Conversation.parse_raw(row.data) if row else None

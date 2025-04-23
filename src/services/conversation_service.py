from uuid import UUID
from src.models.schemas import Conversation, Message, MessageCreate
from src.db.repository import ConversationRepository
from src.providers.interface import LLMClient
from src.core.config import get_settings

class ConversationService:
    def __init__(self, repo: ConversationRepository, llm: LLMClient):
        self.repo = repo
        self.llm = llm
        self.settings = get_settings()

    async def create_conversation(self) -> Conversation:
        conv = Conversation()
        await self.repo.save(conv)
        return conv

    async def handle_message(self, conv_id: UUID, msg_in: MessageCreate) -> Message:
        # Recuperar historial
        conv = await self.repo.get(conv_id)
        user_msg = Message(**msg_in.dict())
        conv.messages.append(user_msg)

        # Llamar al LLM
        context = conv.messages
        assistant_msg = await self.llm.generate(context)
        conv.messages.append(assistant_msg)

        # Guardar cambios
        await self.repo.save(conv)
        return assistant_msg

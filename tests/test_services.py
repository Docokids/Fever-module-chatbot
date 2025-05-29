import pytest
from uuid import UUID, uuid4
from datetime import datetime
from src.services.conversation_service import ConversationService
from src.models.schemas import Message, Conversation, MessageCreate
from src.providers.interface import LLMClient

class MockLLMClient(LLMClient):
    async def generate(self, context):
        return Message(id=uuid4(), role="assistant", content="Test response", timestamp=datetime.now())

class MockRepository:
    def __init__(self):
        self.conversations = {}
    
    async def create(self, conversation):
        conversation.id = uuid4()  # Ensure ID is set
        self.conversations[str(conversation.id)] = conversation
        return conversation
    
    async def get(self, conv_id):
        return self.conversations.get(str(conv_id))
    
    async def add_message(self, conv_id, message):
        conv = await self.get(conv_id)
        if not conv:
            raise KeyError(f"Conversation {conv_id} not found")
        message.id = uuid4()  # Ensure ID is set
        message.timestamp = datetime.now()  # Ensure timestamp is set
        conv.messages.append(message)
        return message
    
    async def list_all(self):
        return list(self.conversations.values())

@pytest.fixture
def mock_repo():
    return MockRepository()

@pytest.fixture
def mock_llm():
    return MockLLMClient()

@pytest.fixture
def service(mock_repo, mock_llm):
    return ConversationService(mock_repo, mock_llm)

@pytest.mark.asyncio
async def test_create_conversation(service):
    # Test creación de conversación
    conv = await service.create_conversation()
    assert isinstance(conv.id, UUID)
    assert len(conv.messages) == 0

@pytest.mark.asyncio
async def test_handle_message(service):
    # Test manejo de mensaje
    conv = await service.create_conversation()
    message = MessageCreate(content="Test message", role="user")
    
    response = await service.handle_message(conv.id, message)
    assert response.role == "assistant"
    assert "Test response" in response.content

@pytest.mark.asyncio
async def test_get_conversation(service):
    # Test obtención de conversación
    conv = await service.create_conversation()
    retrieved = await service.get_conversation(conv.id)
    assert retrieved.id == conv.id
    assert len(retrieved.messages) == 0

@pytest.mark.asyncio
async def test_get_nonexistent_conversation(service):
    # Test obtención de conversación inexistente
    with pytest.raises(KeyError):
        await service.get_conversation(uuid4()) 
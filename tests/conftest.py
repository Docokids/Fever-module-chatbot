# tests/conftest.py
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Agregar el directorio raíz al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.main import app
from src.db.deps import get_redis_repo, get_postgres_repo
from src.repositories.conversation_repository import ConversationRepository

# Fake repo en memoria para tests
class InMemoryRepo(ConversationRepository):
    def __init__(self):
        self.store = {}
        super().__init__(None)  # No necesitamos una sesión real para el repo en memoria

    async def save(self, conv): 
        self.store[str(conv.id)] = conv
        return conv
        
    async def get(self, conv_id): 
        return self.store.get(str(conv_id))

@pytest.fixture
def client():
    # Override dependency
    app.dependency_overrides[get_redis_repo] = lambda: InMemoryRepo()
    app.dependency_overrides[get_postgres_repo] = lambda: InMemoryRepo()
    return TestClient(app)

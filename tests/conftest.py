# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.db.deps import get_redis_repo, get_postgres_repo
from src.db.redis_repository import RedisConversationRepository

# Fake repo en memoria para tests
class InMemoryRepo(RedisConversationRepository):
    def __init__(self):
        self.store = {}

    async def save(self, conv): self.store[str(conv.id)] = conv
    async def get(self, conv_id): return self.store.get(str(conv_id))

@pytest.fixture
def client():
    # Override dependency
    app.dependency_overrides[get_redis_repo] = lambda: InMemoryRepo()
    return TestClient(app)

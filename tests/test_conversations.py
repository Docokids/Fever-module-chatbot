# tests/test_conversations.py
import pytest
from uuid import UUID

def test_create_and_get_history(client):
    # Crear conversación
    res = client.post("/conversations")
    assert res.status_code == 200
    conv = res.json()
    conv_id = conv["id"]

    # Historia inicial vacía
    res = client.get(f"/conversations/{conv_id}/history")
    assert res.json()["messages"] == []

def test_post_message_and_response(client, monkeypatch):
    # Mock LLM generate para devolver mensaje fijo
    from src.providers.interface import LLMClient
    async def fake_generate(self, context): 
        from src.models.schemas import Message
        return Message(role="assistant", content="Respuesta test")

    monkeypatch.setattr(LLMClient, "generate", fake_generate)

    # Crear y enviar mensaje
    conv = client.post("/conversations").json()
    res = client.post(f"/conversations/{conv['id']}/messages", json={"content":"hola"})
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "assistant"
    assert "Respuesta test" in data["content"]

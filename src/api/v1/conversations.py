# src/api/v1/conversations.py
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.models.schemas import Conversation, Message, MessageCreate
from src.services.conversation_service import ConversationService
from src.db.session import get_repository
from src.providers.factory import get_llm_client

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Dependency Injection: repositorio y cliente LLM
def get_service(repo=Depends(get_repository), llm=Depends(get_llm_client)):
    return ConversationService(repo, llm)

@router.post("", response_model=Conversation, summary="Iniciar nueva conversación")
async def create_conversation(service: ConversationService = Depends(get_service)):
    """
    Crea una nueva conversación y devuelve su ID
    """
    return await service.create_conversation()

@router.post("/{conv_id}/messages", response_model=Message, summary="Enviar mensaje de usuario")
async def post_message(
    conv_id: UUID,
    msg: MessageCreate,
    service: ConversationService = Depends(get_service)
):
    """
    Envía un mensaje de rol 'user', obtiene la respuesta del LLM y la devuelve.
    """
    try:
        return await service.handle_message(conv_id, msg)
    except KeyError:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

@router.get("/{conv_id}/history", response_model=Conversation, summary="Obtener historial")
async def get_history(
    conv_id: UUID,
    service: ConversationService = Depends(get_service)
):
    """
    Recupera todo el historial de mensajes de la conversación.
    """
    conv = await service.repo.get(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    return conv

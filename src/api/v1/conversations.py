# src/api/v1/conversations.py
from fastapi import APIRouter, Depends, status
from uuid import UUID
from pydantic import BaseModel
from typing import List
from src.models.schemas import ConversationResponse, MessageResponse, MessageCreate, ConversationListItem
from src.services.conversation_service import ConversationService
from src.db.session import get_repository
from src.providers.factory import get_llm_client
from src.core.exceptions import NotFoundError, ValidationError, InternalServerError

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Dependency Injection: repositorio y cliente LLM
def get_service(repo=Depends(get_repository), llm=Depends(get_llm_client)):
    return ConversationService(repo, llm)

@router.get(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar nueva conversación",
    openapi_extra={
        "requestBody": None
    }
)
async def create_conversation(
    service: ConversationService = Depends(get_service)
):
    """
    Crea una nueva conversación y devuelve su ID.
    Usa la configuración por defecto del sistema.
    """
    try:
        conv = await service.create_conversation(None)
        return ConversationResponse(id=conv.id, messages=[])
    except Exception as e:
        raise InternalServerError(
            message="Error al crear la conversación",
            details={"error": str(e)}
        )

@router.post(
    "/{conv_id}/messages",
    response_model=MessageResponse,
    summary="Enviar mensaje de usuario",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                            "msg": {
                                "role": "user",
                                "content": "¿Cómo tratarías la fiebre en un bebé?"
                        }
                    }
                }
            }
        }
    }
)
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
        raise NotFoundError(
            message="Conversación no encontrada",
            details={"conversation_id": str(conv_id)}
        )
    except ValueError as e:
        raise ValidationError(
            message=str(e),
            details={"conversation_id": str(conv_id)}
        )

@router.get(
    "/{conv_id}/history",
    response_model=ConversationResponse,
    summary="Obtener historial",
    openapi_extra={
        "requestBody": None
    }
)
async def get_history(
    conv_id: UUID,
    service: ConversationService = Depends(get_service)
):
    """
    Recupera todo el historial de mensajes de la conversación.
    """
    try:
        conv = await service.get_conversation(conv_id)
        return ConversationResponse(
            id=conv.id,
            messages=[MessageResponse.from_orm(msg) for msg in conv.messages]
        )
    except KeyError:
        raise NotFoundError(
            message="Conversación no encontrada",
            details={"conversation_id": str(conv_id)}
        )
    except Exception as e:
        raise InternalServerError(
            message="Error al obtener el historial",
            details={"conversation_id": str(conv_id), "error": str(e)}
        )

@router.get(
    "/",
    response_model=List[ConversationListItem],
    summary="Listar todas las conversaciones",
    openapi_extra={
        "requestBody": None
    }
)
async def list_conversations(
    service: ConversationService = Depends(get_service)
):
    """
    Lista todas las conversaciones con información resumida:
    - ID de la conversación
    - Cantidad de mensajes
    - Timestamp del último mensaje
    """
    try:
        return await service.list_conversations()
    except Exception as e:
        raise InternalServerError(
            message="Error al listar las conversaciones",
            details={"error": str(e)}
        )

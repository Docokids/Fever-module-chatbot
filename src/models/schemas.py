# src/models/schemas.py
from typing import List, Literal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class MessageCreate(BaseModel):
    role: Literal["user","assistant"] = "user"
    content: str = Field(..., example="¿Cómo tratarías la fiebre en un bebé?")

class Message(MessageCreate):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Conversation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    messages: List[Message] = []

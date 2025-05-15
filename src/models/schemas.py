# src/models/schemas.py
from typing import List, Literal
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    role = Column(Enum("user", "assistant", name="message_role"), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation_id = Column(PGUUID(as_uuid=True), ForeignKey("conversations.id"))

    conversation = relationship("Conversation", back_populates="messages")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

# Pydantic models for API
from pydantic import BaseModel, Field

class MessageCreate(BaseModel):
    role: Literal["user", "assistant"] = "user"
    content: str = Field(..., example="¿Cómo tratarías la fiebre en un bebé?")

class MessageResponse(MessageCreate):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ConversationListItem(BaseModel):
    id: UUID
    message_count: int
    last_message_timestamp: datetime | None = None

    class Config:
        from_attributes = True

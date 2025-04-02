from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

from src.model.message.message_id import MessageId


class MessageRole(str, Enum):
    """
    Enum representing the role of a message in a conversation with an LLM.
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """
    Value object representing a message in a conversation with an LLM.
    """
    id: Optional[MessageId] = None
    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")
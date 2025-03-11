from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """
    Represents a message in a conversation with an LLM.
    """
    role: str  # 'system', 'user', or 'assistant'
    content: str

    @classmethod
    def system(cls, content: str) -> 'Message':
        """
        Creates a system message.
        """
        return cls(role="system", content=content)

    @classmethod
    def user(cls, content: str) -> 'Message':
        """
        Creates a user message.
        """
        return cls(role="user", content=content)

    @classmethod
    def assistant(cls, content: str) -> 'Message':
        """
        Creates an assistant message.
        """
        return cls(role="assistant", content=content)
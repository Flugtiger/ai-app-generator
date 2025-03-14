from typing import Literal, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """
    Value object representing a message in a conversation with an LLM.
    """
    role: Literal["system", "user", "assistant"]
    content: str
    name: Optional[str] = None

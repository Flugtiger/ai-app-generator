from pydantic import BaseModel, Field
from typing import Optional

from src.model.command.command_id import CommandId


class Command(BaseModel):
    """
    Represents a specific type of interaction in the software System.
    Has a name and a description.
    """
    id: Optional[CommandId] = None
    name: str = Field(..., description="The name of the command")
    description: str = Field(..., description="The description of the command")
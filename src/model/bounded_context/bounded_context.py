from typing import List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field, validator

from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.command.command import Command


class BoundedContext(BaseModel):
    """
    Represents a Bounded Context in Domain-Driven Design.
    A Bounded Context has a unique name and ID, and can contain
    model requirements and commands.
    """
    id: BoundedContextId
    name: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, name: str, id: Optional[BoundedContextId] = None, **data):
        """
        Creates a new BoundedContext with the given name.
        If no ID is provided, a new one is generated.
        """
        if id is None:
            id = BoundedContextId.generate()
        super().__init__(id=id, name=name, **data)

    def update_name(self, new_name: str) -> None:
        """
        Updates the name of the Bounded Context.
        """
        assert new_name, "Name cannot be empty"
        self.name = new_name

    def create_model_requirement(self, requirement_text: str) -> ModelRequirement:
        """
        Creates a new ModelRequirement associated with this BoundedContext.
        """
        return ModelRequirement(
            bounded_context_id=self.id,
            requirement_text=requirement_text
        )

    def create_command(self, name: str, description: str) -> Command:
        """
        Creates a new Command associated with this BoundedContext.
        """
        return Command(
            bounded_context_id=self.id,
            name=name,
            description=description
        )
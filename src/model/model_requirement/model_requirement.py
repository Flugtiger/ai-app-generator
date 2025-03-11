from uuid import uuid4
from pydantic import BaseModel, Field

from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    A ModelRequirement is associated with a BoundedContext and contains
    text that describes the requirement.
    """
    id: ModelRequirementId
    bounded_context_id: BoundedContextId
    requirement_text: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, bounded_context_id: BoundedContextId, requirement_text: str, id: ModelRequirementId = None, **data):
        """
        Creates a new ModelRequirement with the given bounded_context_id and requirement_text.
        If no ID is provided, a new one is generated.
        """
        if id is None:
            id = ModelRequirementId.generate()
        super().__init__(id=id, bounded_context_id=bounded_context_id, requirement_text=requirement_text, **data)
from pydantic import BaseModel, Field
from typing import ClassVar
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    Contains arbitrary text that describes the requirement.
    """
    id: ModelRequirementId
    requirement_text: str

    # Class variable to track the last used number for auto-incrementing IDs
    _last_id_number: ClassVar[int] = 0

    def __init__(self, **data):
        """
        Initialize a new ModelRequirement.
        If no ID is provided, a new one will be generated.
        """
        if 'id' not in data:
            ModelRequirement._last_id_number += 1
            data['id'] = ModelRequirementId(f"MR-{ModelRequirement._last_id_number}")
        
        super().__init__(**data)

    class Config:
        arbitrary_types_allowed = True
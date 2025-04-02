from pydantic import BaseModel, Field
from typing import Optional

from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    Contains arbitrary text that describes the requirement.
    """
    id: Optional[ModelRequirementId] = None
    requirement_text: str = Field(..., description="The text describing the requirement")
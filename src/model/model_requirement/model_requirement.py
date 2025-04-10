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
    implemented: bool = Field(default=False, description="Flag indicating if the requirement has been implemented")
    
    def implement(self) -> None:
        """
        Marks the requirement as implemented by setting the implemented flag to True.
        """
        self.implemented = True

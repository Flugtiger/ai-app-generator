from pydantic import BaseModel, Field
from typing import Optional

from src.model.infrastructure_requirement.infrastructure_requirement_id import InfrastructureRequirementId


class InfrastructureRequirement(BaseModel):
    """
    Represents a requirement for the infrastructure code of the application.
    Contains arbitrary text that describes the requirement.
    """
    id: Optional[InfrastructureRequirementId] = None
    requirement_text: str = Field(..., description="The text describing the infrastructure requirement")
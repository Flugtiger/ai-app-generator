from pydantic import BaseModel, Field
from typing import List, Optional

from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    Contains arbitrary text that describes the requirement.
    """
    id: Optional[ModelRequirementId] = None
    requirement_text: str = Field(..., description="The text describing the requirement")
    implemented: bool = Field(default=False, description="Flag indicating if the requirement has been implemented")
    implementation_file_paths: List[str] = Field(default_factory=list)

    def implement(self, file_paths: List[str]) -> None:
        """
        Marks the requirement as implemented by setting the implemented flag to true
        and storing the file paths where the requirement is implemented.

        Args:
            file_paths: List of file paths where the requirement is implemented
        """
        assert file_paths, "At least one file path must be provided for implementation"

        self.implementation_file_paths = file_paths
        self.implemented = True

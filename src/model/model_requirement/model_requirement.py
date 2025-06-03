from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

from src.model.model_requirement.model_requirement_id import ModelRequirementId


class RequirementState(str, Enum):
    """
    Represents the state of a model requirement.
    """
    IMPLEMENTED = "implemented"
    UPDATED = "updated"
    UNIMPLEMENTED = "unimplemented"


class ModelRequirement(BaseModel):
    """
    Represents a requirement for a DDD model.
    Contains arbitrary text that describes the requirement.
    """
    id: Optional[ModelRequirementId] = None
    requirement_text: str = Field(..., description="The text describing the requirement")
    implemented: bool = Field(default=False, description="Flag indicating if the requirement has been implemented")
    implementation_file_paths: List[str] = Field(default_factory=list)
    implemented_requirement_text: Optional[str] = Field(default=None, description="The requirement text that was implemented")

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
        self.implemented_requirement_text = self.requirement_text

    def update_text(self, new_requirement_text: str) -> None:
        """
        Updates the requirement text.
        If the requirement was previously implemented, it will be marked as updated.

        Args:
            new_requirement_text: The new requirement text
        """
        if self.implemented and self.requirement_text == self.implemented_requirement_text:
            self.implemented_requirement_text = self.requirement_text
            
        self.requirement_text = new_requirement_text
        
        # If the requirement was implemented but the text changed, it's no longer implemented
        if self.implemented_requirement_text and self.requirement_text != self.implemented_requirement_text:
            self.implemented = False

    @property
    def state(self) -> RequirementState:
        """
        Returns the state of the requirement.
        
        Returns:
            RequirementState.IMPLEMENTED if the current requirement text is implemented
            RequirementState.UPDATED if a previous requirement text was implemented
            RequirementState.UNIMPLEMENTED if the requirement wasn't implemented at all
        """
        if self.implemented:
            return RequirementState.IMPLEMENTED
        elif self.implemented_requirement_text:
            return RequirementState.UPDATED
        else:
            return RequirementState.UNIMPLEMENTED

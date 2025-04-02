from pydantic import BaseModel, Field

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class CreateModelRequirementInput(BaseModel):
    """
    Input DTO for creating a model requirement
    """
    requirementText: str = Field(..., description="The text describing the model requirement")


class CreateModelRequirementOutput(BaseModel):
    """
    Output DTO containing the ID of the created model requirement
    """
    modelRequirementId: str


class CreateModelRequirementHandler:
    """
    Handler for creating a new model requirement
    """
    
    def __init__(self, model_requirement_repository: ModelRequirementRepository):
        """
        Initialize the handler with required dependencies
        """
        self.model_requirement_repository = model_requirement_repository
    
    def handle(self, input_dto: CreateModelRequirementInput) -> CreateModelRequirementOutput:
        """
        Creates a new model requirement with the given text
        """
        # Create a new model requirement
        model_requirement = ModelRequirement(
            requirement_text=input_dto.requirementText
        )
        
        # Save the model requirement to the repository
        saved_requirement = self.model_requirement_repository.save(model_requirement)
        
        # Return the ID of the created model requirement
        return CreateModelRequirementOutput(
            modelRequirementId=str(saved_requirement.id.value)
        )
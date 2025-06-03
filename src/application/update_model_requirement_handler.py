from pydantic import BaseModel, Field

from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class UpdateModelRequirementInput(BaseModel):
    """
    Input DTO for updating a model requirement.
    """
    requirementId: str = Field(..., description="The ID of the model requirement to update")
    requirementText: str = Field(..., description="The new text describing the model requirement")


class UpdateModelRequirementOutput(BaseModel):
    """
    Output DTO for updating a model requirement.
    """
    modelRequirementId: str = Field(..., description="The ID of the updated model requirement")
    state: str = Field(..., description="The state of the model requirement after update")


class UpdateModelRequirementHandler:
    """
    Handler for updating a model requirement.
    """

    def __init__(self, model_requirement_repository: ModelRequirementRepository):
        """
        Initialize the handler with dependencies.

        Args:
            model_requirement_repository: Repository for model requirements
        """
        self.model_requirement_repository = model_requirement_repository

    def handle(self, input_dto: UpdateModelRequirementInput) -> UpdateModelRequirementOutput:
        """
        Updates a model requirement with new text.

        Args:
            input_dto: The input data

        Returns:
            Output DTO with the ID of the updated model requirement and its state
        """
        # Get the requirement from the repository
        requirement_id = ModelRequirementId(value=input_dto.requirementId)
        requirement = self.model_requirement_repository.get_by_id(requirement_id)

        # Update the requirement text
        requirement.update_text(input_dto.requirementText)

        # Save the updated requirement
        self.model_requirement_repository.save(requirement)

        # Return the output DTO
        return UpdateModelRequirementOutput(
            modelRequirementId=str(requirement.id),
            state=requirement.state.value
        )

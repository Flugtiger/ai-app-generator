from pydantic import BaseModel
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class CreateModelRequirementInput(BaseModel):
    """Input data for creating a model requirement"""
    requirementText: str


class CreateModelRequirementOutput(BaseModel):
    """Output data after creating a model requirement"""
    requirement_id: str


class ModelRequirementCommands:
    """
    Application service for model requirement commands
    """

    def __init__(self, model_requirement_repository: ModelRequirementRepository):
        """
        Initialize the service with required dependencies

        Args:
            model_requirement_repository: Repository for model requirements
        """
        self.model_requirement_repository = model_requirement_repository

    def create_model_requirement(self, input_data: CreateModelRequirementInput) -> CreateModelRequirementOutput:
        """
        Creates a new model requirement with the provided text

        Args:
            input_data: The input containing the requirement text

        Returns:
            Output containing the ID of the created requirement
        """
        # Create a new model requirement
        model_requirement = ModelRequirement(requirement_text=input_data.requirementText)

        # Save it to the repository
        self.model_requirement_repository.save(model_requirement)

        # Return the ID of the created requirement
        return CreateModelRequirementOutput(requirement_id=str(model_requirement.id))

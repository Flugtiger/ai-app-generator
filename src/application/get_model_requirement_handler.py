from pydantic import BaseModel, Field

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class GetModelRequirementInput(BaseModel):
    """
    Input DTO for retrieving a model requirement by ID
    """
    modelRequirementId: str = Field(..., description="The ID of the model requirement to retrieve")


class GetModelRequirementOutput(BaseModel):
    """
    Output DTO containing the retrieved model requirement details
    """
    modelRequirementId: str
    requirementText: str
    state: str


class GetModelRequirementHandler:
    """
    Handler for retrieving a model requirement by its ID
    """
    
    def __init__(self, model_requirement_repository: ModelRequirementRepository):
        """
        Initialize the handler with required dependencies
        """
        self.model_requirement_repository = model_requirement_repository
    
    def handle(self, input_dto: GetModelRequirementInput) -> GetModelRequirementOutput:
        """
        Retrieves a model requirement by its ID
        """
        # Create a model requirement ID value object
        model_requirement_id = ModelRequirementId(value=input_dto.modelRequirementId)
        
        # Retrieve the model requirement from the repository
        model_requirement = self.model_requirement_repository.get_by_id(model_requirement_id)
        
        # Return the model requirement details
        return GetModelRequirementOutput(
            modelRequirementId=str(model_requirement.id.value),
            requirementText=model_requirement.requirement_text,
            state=model_requirement.state.value
        )

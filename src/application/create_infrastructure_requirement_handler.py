from pydantic import BaseModel, Field

from src.model.infrastructure_requirement.infrastructure_requirement import InfrastructureRequirement
from src.model.infrastructure_requirement.infrastructure_requirement_repository import InfrastructureRequirementRepository


class CreateInfrastructureRequirementInput(BaseModel):
    """
    Input DTO for creating an infrastructure requirement
    """
    requirementText: str = Field(..., description="The text describing the infrastructure requirement")


class CreateInfrastructureRequirementOutput(BaseModel):
    """
    Output DTO containing the ID of the created infrastructure requirement
    """
    infrastructureRequirementId: str


class CreateInfrastructureRequirementHandler:
    """
    Handler for creating a new infrastructure requirement
    """
    
    def __init__(self, infrastructure_requirement_repository: InfrastructureRequirementRepository):
        """
        Initialize the handler with required dependencies
        """
        self.infrastructure_requirement_repository = infrastructure_requirement_repository
    
    def handle(self, input_dto: CreateInfrastructureRequirementInput) -> CreateInfrastructureRequirementOutput:
        """
        Creates a new infrastructure requirement with the given text
        """
        # Create a new infrastructure requirement
        infrastructure_requirement = InfrastructureRequirement(
            requirement_text=input_dto.requirementText
        )
        
        # Save the infrastructure requirement to the repository
        saved_requirement = self.infrastructure_requirement_repository.save(infrastructure_requirement)
        
        # Return the ID of the created infrastructure requirement
        return CreateInfrastructureRequirementOutput(
            infrastructureRequirementId=str(saved_requirement.id.value)
        )
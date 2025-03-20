from pydantic import BaseModel
from typing import Optional

from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.infra_requirement.infra_requirement_id import InfraRequirementId
from src.model.infra_requirement.infra_requirement_repository import InfraRequirementRepository


class CreateInfraRequirementInput(BaseModel):
    """
    Input data for creating a new infrastructure requirement.
    """
    requirement_text: str


class CreateInfraRequirementOutput(BaseModel):
    """
    Output data after creating a new infrastructure requirement.
    """
    id: str
    requirement_text: str


class InfraRequirementCommands:
    """
    Application service for infrastructure requirement commands.
    """

    def __init__(self, infra_requirement_repository: InfraRequirementRepository):
        """
        Initialize the application service with required dependencies.

        Args:
            infra_requirement_repository: Repository for infrastructure requirements.
        """
        self.infra_requirement_repository = infra_requirement_repository

    def create_infra_requirement(self, input_data: CreateInfraRequirementInput) -> CreateInfraRequirementOutput:
        """
        Create a new infrastructure requirement.

        Args:
            input_data: Input data containing the requirement text.

        Returns:
            Output data containing the ID and requirement text of the created requirement.
        """
        # Create a new infrastructure requirement
        infra_requirement = InfraRequirement(
            requirement_text=input_data.requirement_text
        )

        # Save the infrastructure requirement
        self.infra_requirement_repository.save(infra_requirement)

        # Return the output
        return CreateInfraRequirementOutput(
            id=infra_requirement.id.value,
            requirement_text=infra_requirement.requirement_text
        )

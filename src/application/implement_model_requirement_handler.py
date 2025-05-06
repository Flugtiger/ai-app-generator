from pydantic import BaseModel, Field
from typing import Optional

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.generators.domain_model_generator import DomainModelGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService


class ImplementModelRequirementInput(BaseModel):
    """
    Input DTO for implementing a single model requirement
    """
    requirementId: str = Field(..., description="The ID of the requirement to implement")
    targetDirectory: Optional[str] = Field(
        "generated", description="The directory where the generated files will be written")


class ImplementModelRequirementOutput(BaseModel):
    """
    Output DTO containing the number of modified files
    """
    numberOfFiles: int
    requirementId: str


class ImplementModelRequirementHandler:
    """
    Handler for implementing a single model requirement in the existing domain model
    """

    def __init__(
        self,
        model_requirement_repository: ModelRequirementRepository,
        domain_model_generator: DomainModelGenerator,
        domain_model_files_service: DomainModelFilesService
    ):
        """
        Initialize the handler with required dependencies
        """
        self.model_requirement_repository = model_requirement_repository
        self.domain_model_generator = domain_model_generator
        self.domain_model_files_service = domain_model_files_service

    def handle(self, input_dto: ImplementModelRequirementInput) -> ImplementModelRequirementOutput:
        """
        Implements a single model requirement in the existing domain model.
        Reads the current domain model files, applies the requirement, and writes the updated files.
        After implementation, marks the requirement as implemented.
        """
        # Get the requirement from the repository
        requirement_id = ModelRequirementId(value=input_dto.requirementId)
        requirement = self.model_requirement_repository.get_by_id(requirement_id)

        # Read existing domain model files
        existing_domain_model = self.domain_model_files_service.read_files(input_dto.targetDirectory)

        # Implement the requirement in the domain model
        updated_domain_model = self.domain_model_generator.implement(requirement, existing_domain_model)

        # Write the updated domain model files
        self.domain_model_files_service.write_files(input_dto.targetDirectory, updated_domain_model)

        # Mark the requirement as implemented
        requirement.implement(list(updated_domain_model.get_all_files().keys()))
        self.model_requirement_repository.save(requirement)

        # Return the number of modified files
        return ImplementModelRequirementOutput(
            numberOfFiles=len(updated_domain_model.get_all_files()),
            requirementId=input_dto.requirementId
        )

from pydantic import BaseModel, Field
from typing import Optional, List

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.generators.domain_model_generator import DomainModelGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService


class GenerateModelInput(BaseModel):
    """
    Input DTO for generating domain model
    """
    targetDirectory: Optional[str] = Field(
        "generated", description="The directory where the generated files will be written")
    useAllRequirements: Optional[bool] = Field(
        False, description="If true, all requirements will be used regardless of implementation status")


class GenerateModelOutput(BaseModel):
    """
    Output DTO containing the number of generated files
    """
    numberOfFiles: int


class GenerateModelHandler:
    """
    Handler for generating the domain model from requirements
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

    def handle(self, input_dto: GenerateModelInput) -> GenerateModelOutput:
        """
        Generates domain model files based on model requirements.
        By default, only uses unimplemented requirements unless useAllRequirements is True.
        After generation, marks all used requirements as implemented.
        """
        # Get model requirements from the repository based on the flag
        if input_dto.useAllRequirements:
            model_requirements = self.model_requirement_repository.get_all()
        else:
            model_requirements = self.model_requirement_repository.get_unimplemented()

        # Generate the domain model files
        domain_model_files = self.domain_model_generator.generate(model_requirements)

        # Write the domain model files to the target directory
        self.domain_model_files_service.write_files(input_dto.targetDirectory, domain_model_files)

        # Mark all used requirements as implemented
        self._mark_requirements_as_implemented(model_requirements)

        # Return the number of generated files
        return GenerateModelOutput(
            numberOfFiles=len(domain_model_files.get_all_files())
        )

    def _mark_requirements_as_implemented(self, requirements: List[ModelRequirement]) -> None:
        """
        Marks all requirements in the list as implemented and saves them to the repository
        """
        for requirement in requirements:
            requirement.implement(["dummy"])
            self.model_requirement_repository.save(requirement)

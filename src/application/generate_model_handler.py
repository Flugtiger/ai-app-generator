from pydantic import BaseModel, Field
from typing import Optional

from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.generators.domain_model_generator import DomainModelGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService


class GenerateModelInput(BaseModel):
    """
    Input DTO for generating domain model
    """
    targetDirectory: Optional[str] = Field("generated", description="The directory where the generated files will be written")


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
        Generates domain model files based on all model requirements
        """
        # Get all model requirements from the repository
        model_requirements = self.model_requirement_repository.get_all()
        
        # Generate the domain model files
        domain_model_files = self.domain_model_generator.generate(model_requirements)
        
        # Write the domain model files to the target directory
        self.domain_model_files_service.write_files(input_dto.targetDirectory, domain_model_files)
        
        # Return the number of generated files
        return GenerateModelOutput(
            numberOfFiles=len(domain_model_files.get_all_files())
        )
from pydantic import BaseModel, Field
from typing import Optional

from src.model.infrastructure_requirement.infrastructure_requirement_repository import InfrastructureRequirementRepository
from src.model.generators.infrastructure_generator import InfrastructureGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService
from src.model.services.infrastructure_files_service import InfrastructureFilesService


class GenerateInfrastructureInput(BaseModel):
    """
    Input DTO for generating infrastructure code
    """
    targetDirectory: Optional[str] = Field("generated", description="The directory where the generated files will be written")


class GenerateInfrastructureOutput(BaseModel):
    """
    Output DTO containing the number of generated files
    """
    numberOfFiles: int


class GenerateInfrastructureHandler:
    """
    Handler for generating the infrastructure code from requirements and domain model
    """
    
    def __init__(
        self, 
        infrastructure_requirement_repository: InfrastructureRequirementRepository,
        infrastructure_generator: InfrastructureGenerator,
        domain_model_files_service: DomainModelFilesService,
        infrastructure_files_service: InfrastructureFilesService
    ):
        """
        Initialize the handler with required dependencies
        """
        self.infrastructure_requirement_repository = infrastructure_requirement_repository
        self.infrastructure_generator = infrastructure_generator
        self.domain_model_files_service = domain_model_files_service
        self.infrastructure_files_service = infrastructure_files_service
    
    def handle(self, input_dto: GenerateInfrastructureInput) -> GenerateInfrastructureOutput:
        """
        Generates infrastructure code based on requirements and the domain model
        """
        # Get all infrastructure requirements from the repository
        infrastructure_requirements = self.infrastructure_requirement_repository.get_all()
        
        # Read the domain model files
        domain_model_files = self.domain_model_files_service.read_files(input_dto.targetDirectory)
        
        # Generate the infrastructure files
        infrastructure_files = self.infrastructure_generator.generate(
            infrastructure_requirements, 
            domain_model_files
        )
        
        # Write the infrastructure files to the target directory
        self.infrastructure_files_service.write_files(input_dto.targetDirectory, infrastructure_files)
        
        # Return the number of generated files
        return GenerateInfrastructureOutput(
            numberOfFiles=len(infrastructure_files.get_all_files())
        )
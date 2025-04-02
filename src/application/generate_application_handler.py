from pydantic import BaseModel, Field
from typing import Optional

from src.model.command.command_repository import CommandRepository
from src.model.files.domain_model_files import DomainModelFiles
from src.model.generators.application_generator import ApplicationGenerator
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.domain_model_files_service import DomainModelFilesService


class GenerateApplicationInput(BaseModel):
    """
    Input DTO for generating application layer
    """
    targetDirectory: Optional[str] = Field("generated", description="The directory where the generated files will be written")


class GenerateApplicationOutput(BaseModel):
    """
    Output DTO containing the number of generated files
    """
    numberOfFiles: int


class GenerateApplicationHandler:
    """
    Handler for generating the application layer from commands
    """
    
    def __init__(
        self, 
        command_repository: CommandRepository,
        application_generator: ApplicationGenerator,
        domain_model_files_service: DomainModelFilesService,
        application_files_service: ApplicationFilesService
    ):
        """
        Initialize the handler with required dependencies
        """
        self.command_repository = command_repository
        self.application_generator = application_generator
        self.domain_model_files_service = domain_model_files_service
        self.application_files_service = application_files_service
    
    def handle(self, input_dto: GenerateApplicationInput) -> GenerateApplicationOutput:
        """
        Generates application layer files based on all commands and the domain model
        """
        # Get all commands from the repository
        commands = self.command_repository.get_all()
        
        # Read the domain model files
        domain_model_files = self.domain_model_files_service.read_files(input_dto.targetDirectory)
        
        # Generate the application files
        application_files = self.application_generator.generate(commands, domain_model_files)
        
        # Write the application files to the target directory
        self.application_files_service.write_files(input_dto.targetDirectory, application_files)
        
        # Return the number of generated files
        return GenerateApplicationOutput(
            numberOfFiles=len(application_files.get_all_files())
        )
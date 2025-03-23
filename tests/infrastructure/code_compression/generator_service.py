import os
from pydantic import BaseModel, Field
from typing import List, Optional

from src.model.command.command_repository import CommandRepository
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository
from src.model.services.application_generator import ApplicationGenerator
from src.model.services.domain_model_generator import DomainModelGenerator
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.domain_model_files_service import DomainModelFilesService


class GenerateApplicationInput(BaseModel):
    """Input data for generating application code."""
    targetDirectory: str = Field(default="generated", description="Directory where generated files will be written")


class GenerateApplicationOutput(BaseModel):
    """Output data after generating application code."""
    numberOfFiles: int = Field(..., description="Number of generated application files")


class GenerateModelInput(BaseModel):
    """Input data for generating domain model code."""
    targetDirectory: str = Field(default="generated", description="Directory where generated files will be written")


class GenerateModelOutput(BaseModel):
    """Output data after generating domain model code."""
    numberOfFiles: int = Field(..., description="Number of generated model files")


class GeneratorService:
    """Service for generating application and domain model code."""
    
    def __init__(
        self,
        command_repository: CommandRepository,
        model_requirement_repository: ModelRequirementRepository,
        application_generator: ApplicationGenerator,
        domain_model_generator: DomainModelGenerator,
        application_files_service: ApplicationFilesService,
        domain_model_files_service: DomainModelFilesService
    ):
        """
        Initialize the generator service.
        
        Args:
            command_repository: Repository for accessing commands
            model_requirement_repository: Repository for accessing model requirements
            application_generator: Service for generating application code
            domain_model_generator: Service for generating domain model code
            application_files_service: Service for reading/writing application files
            domain_model_files_service: Service for reading/writing domain model files
        """
        self.command_repository = command_repository
        self.model_requirement_repository = model_requirement_repository
        self.application_generator = application_generator
        self.domain_model_generator = domain_model_generator
        self.application_files_service = application_files_service
        self.domain_model_files_service = domain_model_files_service
    
    def generate_application(self, input_data: GenerateApplicationInput) -> GenerateApplicationOutput:
        """
        Generate application code from all commands and write to the target directory.
        
        Args:
            input_data: Input containing the target directory
            
        Returns:
            Output containing the number of generated files
        """
        # Get all commands
        commands = self.command_repository.get_all()
        
        # Ensure we have commands to generate from
        if not commands:
            raise ValueError("No commands found to generate application from")
        
        # Read existing domain model files
        domain_model_files = self.domain_model_files_service.read_domain_model_files(os.getcwd())
        
        # Generate application files
        application_files = self.application_generator.generate_application(commands, domain_model_files)
        
        # Ensure target directory exists
        os.makedirs(input_data.targetDirectory, exist_ok=True)
        
        # Write application files to target directory
        self.application_files_service.write_application_files(input_data.targetDirectory, application_files)
        
        # Return the number of generated files
        return GenerateApplicationOutput(numberOfFiles=len(application_files.get_all_paths()))
    
    def generate_model(self, input_data: GenerateModelInput) -> GenerateModelOutput:
        """
        Generate domain model code from all model requirements and write to the target directory.
        
        Args:
            input_data: Input containing the target directory
            
        Returns:
            Output containing the number of generated files
        """
        # Get all model requirements
        model_requirements = self.model_requirement_repository.get_all()
        
        # Ensure we have model requirements to generate from
        if not model_requirements:
            raise ValueError("No model requirements found to generate domain model from")
        
        # Generate domain model files
        domain_model_files = self.domain_model_generator.generate_domain_model(model_requirements)
        
        # Ensure target directory exists
        os.makedirs(input_data.targetDirectory, exist_ok=True)
        
        # Write domain model files to target directory
        self.domain_model_files_service.write_domain_model_files(input_data.targetDirectory, domain_model_files)
        
        # Return the number of generated files
        return GenerateModelOutput(numberOfFiles=len(domain_model_files.get_all_paths()))
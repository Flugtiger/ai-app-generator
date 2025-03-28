from pydantic import BaseModel
from typing import Dict, List
from src.model.command.command_repository import CommandRepository
from src.model.services.application_services_generator.application_services_generator import ApplicationServicesGenerator
from src.model.services.domain_model_files_service import DomainModelFilesService
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.files_dictionary_service import FilesDictionaryService


class GenerateApplicationServicesInput(BaseModel):
    """Input data for generating application services"""
    project_path: str = "generated"


class GenerateApplicationServicesOutput(BaseModel):
    """Output data after generating application services"""
    files_count: int


class ApplicationServicesGeneratorCommands:
    """                                                                                                                                       
    Application service for generating application services from commands                                                                     
    """

    def __init__(
        self,
        command_repository: CommandRepository,
        application_services_generator: ApplicationServicesGenerator
    ):
        """                                                                                                                                   
        Initialize the service with required dependencies                                                                                     

        Args:                                                                                                                                 
            command_repository: Repository for commands                                                                                       
            application_services_generator: Service for generating application services                                                       
        """
        self.command_repository = command_repository
        self.application_services_generator = application_services_generator
        self.domain_model_files_service = DomainModelFilesService()

    def generate_application_services(self, input_data: GenerateApplicationServicesInput) -> GenerateApplicationServicesOutput:
        """                                                                                                                                   
        Generates application services from all the commands and writes them to disk                                                                                  

        Args:                                                                                                                                 
            input_data: The input data containing the project path                                                                                   

        Returns:                                                                                                                              
            Output containing the number of files written                                                                         
        """
        # Get all commands
        commands = self.command_repository.get_all()

        # Read the existing domain model from disk
        domain_model = self.domain_model_files_service.read_from_directory(input_data.project_path)

        # Generate the application services
        app_services = self.application_services_generator.generate_application_services(commands, domain_model)

        # Write the application services to disk
        FilesDictionaryService.write_to_directory(app_services, input_data.project_path)

        # Return the number of files written
        return GenerateApplicationServicesOutput(files_count=len(app_services.files))

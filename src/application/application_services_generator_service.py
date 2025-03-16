from pydantic import BaseModel
from typing import Dict, List
from src.model.command.command_repository import CommandRepository
from src.model.services.application_services_generator.application_services_generator import ApplicationServicesGenerator


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

    def generate_application_services(self, input_data: GenerateApplicationServicesInput) -> GenerateApplicationServicesOutput:
        """                                                                                                                                   
        Generates application services from all the commands                                                                                  

        Args:                                                                                                                                 
            input_data: The input data (empty in this case)                                                                                   

        Returns:                                                                                                                              
            Output containing the generated application service files                                                                         
        """
        # Get all commands
        commands = self.command_repository.get_all()

        # Generate the application services
        domain_model = self.application_services_generator.generate_application_services(commands)

        # Return the generated files
        return GenerateApplicationServicesOutput(files=domain_model.files)

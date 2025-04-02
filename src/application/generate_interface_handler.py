from pydantic import BaseModel, Field
from typing import Optional

from src.model.generators.interface_generator import InterfaceGenerator
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.domain_model_files_service import DomainModelFilesService
from src.model.services.infrastructure_files_service import InfrastructureFilesService
from src.model.services.interface_files_service import InterfaceFilesService


class GenerateInterfaceInput(BaseModel):
    """
    Input DTO for generating interface code
    """
    targetDirectory: Optional[str] = Field("generated", description="The directory where the generated files will be written")


class GenerateInterfaceOutput(BaseModel):
    """
    Output DTO containing the number of generated files
    """
    numberOfFiles: int


class GenerateInterfaceHandler:
    """
    Handler for generating the interface based on domain model, application and infrastructure code
    """
    
    def __init__(
        self, 
        interface_generator: InterfaceGenerator,
        domain_model_files_service: DomainModelFilesService,
        application_files_service: ApplicationFilesService,
        infrastructure_files_service: InfrastructureFilesService,
        interface_files_service: InterfaceFilesService
    ):
        """
        Initialize the handler with required dependencies
        """
        self.interface_generator = interface_generator
        self.domain_model_files_service = domain_model_files_service
        self.application_files_service = application_files_service
        self.infrastructure_files_service = infrastructure_files_service
        self.interface_files_service = interface_files_service
    
    def handle(self, input_dto: GenerateInterfaceInput) -> GenerateInterfaceOutput:
        """
        Generates interface files based on domain model, application and infrastructure code
        """
        # Read the domain model, application, and infrastructure files
        domain_model_files = self.domain_model_files_service.read_files(input_dto.targetDirectory)
        application_files = self.application_files_service.read_files(input_dto.targetDirectory)
        infrastructure_files = self.infrastructure_files_service.read_files(input_dto.targetDirectory)
        
        # Generate the interface files
        interface_files = self.interface_generator.generate(
            application_files,
            domain_model_files,
            infrastructure_files
        )
        
        # Write the interface files to the target directory
        self.interface_files_service.write_files(input_dto.targetDirectory, interface_files)
        
        # Return the number of generated files
        return GenerateInterfaceOutput(
            numberOfFiles=len(interface_files.get_all_files())
        )
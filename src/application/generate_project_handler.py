from pydantic import BaseModel, Field
from typing import Optional

from src.model.generators.project_generator import ProjectGenerator
from src.model.services.infrastructure_files_service import InfrastructureFilesService
from src.model.services.interface_files_service import InterfaceFilesService
from src.model.services.base_files_service import BaseFilesService
from src.model.files.files_dictionary import FilesDictionary


class GenerateProjectInput(BaseModel):
    """
    Input DTO for generating project files
    """
    targetDirectory: Optional[str] = Field("generated", description="The directory where the generated files will be written")


class GenerateProjectOutput(BaseModel):
    """
    Output DTO containing the number of generated files
    """
    numberOfFiles: int


class GenerateProjectHandler:
    """
    Handler for generating the project files for the application
    """
    
    def __init__(
        self, 
        project_generator: ProjectGenerator,
        infrastructure_files_service: InfrastructureFilesService,
        interface_files_service: InterfaceFilesService
    ):
        """
        Initialize the handler with required dependencies
        """
        self.project_generator = project_generator
        self.infrastructure_files_service = infrastructure_files_service
        self.interface_files_service = interface_files_service
    
    def handle(self, input_dto: GenerateProjectInput) -> GenerateProjectOutput:
        """
        Generates project files based on infrastructure and interface code
        """
        # Read the infrastructure and interface files
        infrastructure_files = self.infrastructure_files_service.read_files(input_dto.targetDirectory)
        interface_files = self.interface_files_service.read_files(input_dto.targetDirectory)
        
        # Generate the project files
        project_files = self.project_generator.generate(infrastructure_files, interface_files)
        
        # Create a custom files service for writing the project files
        # since they don't have a specific subfolder
        class ProjectFilesService(BaseFilesService):
            def __init__(self):
                super().__init__("", FilesDictionary)
        
        project_files_service = ProjectFilesService()
        
        # Write the project files to the target directory
        project_files_service.write_files(input_dto.targetDirectory, project_files)
        
        # Return the number of generated files
        return GenerateProjectOutput(
            numberOfFiles=len(project_files.get_all_files())
        )
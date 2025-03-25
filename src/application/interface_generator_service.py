from pydantic import BaseModel
from typing import List

from src.model.services.domain_model_files_service import DomainModelFilesService
from src.model.services.infrastructure_files_service import InfrastructureFilesService
from src.model.services.interface_generator.interface_generator import InterfaceGenerator
from src.model.services.application_files_service import ApplicationFilesService
from src.model.services.files_dictionary_service import FilesDictionaryService
from src.model.value_objects.interface_files import InterfaceFiles


class GenerateInterfaceInput(BaseModel):
    """
    Input data for generating interface code.
    """
    project_root: str


class GenerateInterfaceOutput(BaseModel):
    """
    Output data from generating interface code.
    """
    generated_files: List[str]
    message: str


class InterfaceGeneratorCommands:
    """
    Application service for interface generation commands.
    Provides functionality to generate CLI interfaces based on application services.
    """

    def __init__(
        self,
        interface_generator: InterfaceGenerator
    ):
        """
        Initialize the InterfaceGeneratorCommands service.

        Args:
            interface_generator: The domain service that generates interface code.
        """
        self.interface_generator = interface_generator
        self.application_files_service = ApplicationFilesService()
        self.model_files_service = DomainModelFilesService()
        self.infra_files_service = InfrastructureFilesService()

    def generate_interface(self, input_data: GenerateInterfaceInput) -> GenerateInterfaceOutput:
        """
        Generate CLI interface code based on the application services in the project.

        Args:
            input_data: Input containing the project root directory.

        Returns:
            Output containing the list of generated files and a success message.
        """
        # Read application services from the project
        application_services = self.application_files_service.read_from_directory(input_data.project_root)
        model_files = self.model_files_service.read_from_directory(input_data.project_root)
        infra_files = self.infra_files_service.read_from_directory(input_data.project_root)

        # Generate interface code
        interface_files = self.interface_generator.generate_interface(application_services, model_files, infra_files)

        # Write the generated files to the project
        FilesDictionaryService.write_to_directory(interface_files, input_data.project_root)

        # Return the output
        return GenerateInterfaceOutput(
            generated_files=list(interface_files.files.keys()),
            message="CLI interface generated successfully."
        )

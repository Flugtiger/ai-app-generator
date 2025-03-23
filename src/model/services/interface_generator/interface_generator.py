import os
from pathlib import Path
from typing import List
from src.model.value_objects.application_files import ApplicationFiles
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.infrastructure_files import InfrastructureFiles
from src.model.value_objects.message import Message


class InterfaceGenerator:
    """                                                                                                                                       
    Domain service that generates CLI interface code using a LLM.                                                                       
    Takes the Application Services and generates the appropriate CLI implementation.                                                                    
    """

    def __init__(self, llm_service: LlmService):
        """                                                                                                                                   
        Initialize the InterfaceGenerator with a LLM service.                                                                       

        Args:                                                                                                                                 
            llm_service: The LLM service to use for generating the CLI interface.                                                      
        """
        self.llm_service = llm_service
        self.message_parser = MessageParser()

    def _load_prompt_from_file(self, filename: str) -> str:
        """
        Load system prompt text from a file in the same directory as this class.

        Args:
            filename: The name of the file to load

        Returns:
            The content of the file as a string
        """
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        file_path = current_dir / filename

        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            # Return a default message if the file doesn't exist
            return f"Prompt file '{filename}' not found in {current_dir}"

    def generate_interface(self, application_services: ApplicationFiles) -> InfrastructureFiles:
        """                                                                                                                                   
        Generates CLI interface code based on the provided application services.                                                                        

        Args:                                                                                                                                 
            application_services: The existing application services to reference when generating CLI interface code.                                                                

        Returns:                                                                                                                              
            An InfrastructureFiles object containing the generated CLI interface code.                                                                  
        """
        if not application_services.files:
            raise ValueError("Application services cannot be empty")

        # Prepare the application services files text
        app_services_files = ""
        for path, content in application_services.files.items():
            app_services_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Prepare the system prompt
        roadmap = self._load_prompt_from_file("interface_roadmap.txt")
        philosophy = self._load_prompt_from_file("interface_philosophy.txt")
        system_prompt = "\n\n".join([
            roadmap,
            "The existing application services:",
            app_services_files,
            self.message_parser.get_file_template_with_example(),
            philosophy])

        # Generate the CLI interface using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate CLI interface code based on the application services.")
        ]

        response = self.llm_service.generate_response(messages)

        # Parse the files from the response
        files_dict = self.message_parser.parse_files_from_message(response)

        # Convert to InfrastructureFiles
        infra_files = InfrastructureFiles()

        # Add each file, ensuring they're in the src/infrastructure directory
        for path, content in files_dict.files.items():
            infra_files.add_file(path, content)

        return infra_files

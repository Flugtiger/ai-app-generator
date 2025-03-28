import os
from pathlib import Path
from typing import List
from src.model.command.command import Command
from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.value_objects.domain_model_files import DomainModelFiles
from src.model.value_objects.application_files import ApplicationFiles
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.infrastructure_files import InfrastructureFiles
from src.model.value_objects.message import Message


class InfrastructureGenerator:
    """                                                                                                                                       
    Domain service that generates infrastructure code using a LLM.                                                                       
    Takes the Domain Model and generates the appropriate infrastructure implementation.                                                                    
    """

    def __init__(self, llm_service: LlmService):
        """                                                                                                                                   
        Initialize the InfrastructureGenerator with a LLM service.                                                                       

        Args:                                                                                                                                 
            llm_service: The LLM service to use for generating the infrastructure.                                                      
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

    def generate_infrastructure(self, requirements: List[InfraRequirement], domain_model: DomainModelFiles) -> InfrastructureFiles:
        """                                                                                                                                   
        Generates infrastructure code based on the provided requirements and existing domain model.                                                                        

        Args:                                                                                                                                 
            requirements: The requirements for which to generate infrastructure code.
            domain_model: The existing domain model to reference when generating infrastructure code.                                                                

        Returns:                                                                                                                              
            An InfrastructureFiles object containing the generated infrastructure code.                                                                  
        """
        assert requirements, "Requirements cannot be empty"

        # Prepare the commands text
        requirements_text = "\n".join([req.requirement_text for req in requirements])

        # Prepare the domain model files text
        domain_model_files = ""
        for path, content in domain_model.files.items():
            domain_model_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Prepare the system prompt
        roadmap = self._load_prompt_from_file("infrastructure_roadmap.txt")
        philosophy = self._load_prompt_from_file("infrastructure_philosophy.txt")
        system_prompt = "\n\n".join([
            roadmap,
            "The existing domain model:",
            domain_model_files,
            "The requirements:",
            requirements_text,
            self.message_parser.get_file_template_with_example(),
            philosophy])

        # Generate the application services using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate infrastructure code based on the model and the requirements.")
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

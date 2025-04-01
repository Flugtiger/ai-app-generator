import os
from pathlib import Path
from typing import List
from src.model.command.command import Command
from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.services.code_compression_service import CodeCompressionService
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

    def __init__(self, llm_service: LlmService, code_compression_service: CodeCompressionService):
        """                                                                                                                                   
        Initialize the InfrastructureGenerator with a LLM service.                                                                       

        Args:                                                                                                                                 
            llm_service: The LLM service to use for generating the infrastructure.                                                      
            code_compression_service: The service to compress code before sending to LLM.
        """
        self.llm_service = llm_service
        self.code_compression_service = code_compression_service
        self.message_parser = MessageParser()

    def _load_prompt_from_file(self, filename: str) -> str:
        """
        Load system prompt text from a file in the same directory as this class.

        Args:
            filename: The name of the file to load

        Returns:
            The content of the file as a string
        """
        prompts_dir = Path("resources/prompts")
        file_path = prompts_dir / filename

        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            # Return a default message if the file doesn't exist
            return f"Prompt file '{filename}' not found in {prompts_dir}"

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
        compressed_domain_model = self.code_compression_service.remove_method_bodies(domain_model)
        domain_model_files = ""
        for path, content in compressed_domain_model.files.items():
            domain_model_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Prepare the system prompt
        roadmap = self._load_prompt_from_file("infrastructure_preamble.txt")
        general_prompt = self._load_prompt_from_file("general.txt")
        philosophy = self._load_prompt_from_file("infrastructure_requirements.txt")

        system_prompt = "\n\n".join([
            roadmap,
            general_prompt,
            self.message_parser.get_file_template_with_example(),
            philosophy])

        user_prompt = "\n".join([
            "The signatures of the existing domain model (method bodies removed intentionally):",
            domain_model_files,
            "The requirements:",
            requirements_text,
            "Please generate infrastructure code based on the model and the requirements."])

        # Generate the application services using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=user_prompt)
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

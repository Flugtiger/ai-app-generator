import logging
import os
from pathlib import Path
from typing import List
from src.model.command.command import Command
from src.model.value_objects.domain_model_files import DomainModelFiles
from src.model.value_objects.application_files import ApplicationFiles
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.message import Message
from src.model.services.code_compression_service import CodeCompressionService

logger = logging.getLogger(__name__)


class ApplicationServicesGenerator:
    """                                                                                                                                       
    Domain service that generates application service code using a LLM.                                                                       
    Takes Command entities and generates appropriate application services.                                                                    
    """

    def __init__(self, llm_service: LlmService, code_compression_service: CodeCompressionService):
        """                                                                                                                                   
        Initialize the ApplicationServicesGenerator with a LLM service and code compression service.                                                                       

        Args:                                                                                                                                 
            llm_service: The LLM service to use for generating the application services.
            code_compression_service: The service to compress code before sending to LLM.
        """
        self.llm_service = llm_service
        self.message_parser = MessageParser()
        self.code_compression_service = code_compression_service

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

    def generate_application_services(self, commands: List[Command], domain_model: DomainModelFiles) -> ApplicationFiles:
        """                                                                                                                                   
        Generates application services based on the provided commands and existing domain model.                                                                        

        Args:                                                                                                                                 
            commands: The commands for which to generate application services.
            domain_model: The existing domain model to reference when generating application services.                                                                

        Returns:                                                                                                                              
            An ApplicationServices containing the generated application service code.                                                                  
        """
        assert commands, "Commands cannot be empty"

        # Prepare the commands text
        commands_text = "\n".join([f"{cmd.id.value}: {cmd.name} - {cmd.description}" for cmd in commands])

        # Compress the domain model files by removing method bodies
        compressed_domain_model = self.code_compression_service.remove_method_bodies(domain_model)

        # Prepare the compressed domain model files text
        domain_model_files = ""
        for path, content in compressed_domain_model.files.items():
            domain_model_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Prepare the system prompt
        roadmap = self._load_prompt_from_file("application_preamble.txt")
        general_prompt = self._load_prompt_from_file("general.txt")
        philosophy = self._load_prompt_from_file("application_requirements.txt")

        system_prompt = "\n\n".join([
            roadmap,
            general_prompt,
            self.message_parser.get_file_template_with_example(),
            philosophy])

        user_prompt = "\n".join(
            "The signatures of the existing domain model (method bodies removed intentionally):",
            domain_model_files,
            "The commands:",
            commands_text,
            "Please generate application services based on the commands.")

        # Generate the application services using the LLM
        logger.debug("Gen App System prompt:\n%s", system_prompt)
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=user_prompt)
        ]

        response = self.llm_service.generate_response(messages)

        # Parse the files from the response
        files_dict = self.message_parser.parse_files_from_message(response)

        # Convert to ApplicationServices
        app_services = ApplicationFiles()

        # Add each file, ensuring they're in the src/application directory
        for path, content in files_dict.files.items():
            # If the path doesn't start with src/application/, modify it
            if not path.startswith('src/application/'):
                # Extract the filename and add it to src/application/
                filename = Path(path).name
                path = f"src/application/{filename}"

            app_services.add_file(path, content)

        return app_services

    def modify_application_services(self, commands: List[Command], current_services: ApplicationFiles) -> ApplicationFiles:
        """                                                                                                                                   
        Modifies existing application services based on the provided commands.                                                                

        Args:                                                                                                                                 
            commands: The commands for which to modify application services.                                                                  
            current_services: The current application services to modify.                                                

        Returns:                                                                                                                              
            An ApplicationServices containing the modified application service code.                                                                   
        """
        assert commands, "Commands cannot be empty"
        assert current_services, "Current model cannot be empty"

        # Prepare the commands text
        commands_text = "\n".join([f"{cmd.id.value}: {cmd.name} - {cmd.description}" for cmd in commands])

        # Compress the current application services files by removing method bodies
        compressed_services = self.code_compression_service.remove_method_bodies(current_services)

        # Prepare the compressed application services files
        current_files = ""
        for path, content in compressed_services.files.items():
            current_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Prepare the system prompt
        roadmap = self._load_prompt_from_file("application_services_modifier_roadmap.txt")
        philosophy = self._load_prompt_from_file("application_services_philosophy.txt")
        system_prompt = "\n\n".join([
            roadmap,
            "The commands:",
            commands_text,
            "Here are the current application services:",
            current_files,
            self.message_parser.get_diff_template_with_example(),
            philosophy])

        # Generate the application service modifications using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate the necessary changes to the application services based on the commands.")
        ]

        response = self.llm_service.generate_response(messages)

        # Parse the diffs from the response
        diffs = self.message_parser.parse_diffs_from_message(response)

        # Create a new application services as a copy of the current one
        modified_services = current_services.copy()
        modified_services.apply_diff()

        # Apply the diffs to the application services
        for filename, diff_content in diffs.items():
            modified_services.apply_diff(diff_content)

        return modified_services

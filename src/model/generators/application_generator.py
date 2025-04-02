import os
from typing import List

from src.model.command.command import Command
from src.model.files.application_files import ApplicationFiles
from src.model.files.domain_model_files import DomainModelFiles
from src.model.message.message import Message, MessageRole
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser


class ApplicationGenerator:
    """
    Generator service that uses a LLM to generate application files based on commands and domain model.
    """
    
    def __init__(self, llm_service: LLMService, message_parser: MessageParser):
        """
        Initializes the generator with the necessary services.
        """
        self.llm_service = llm_service
        self.message_parser = message_parser
        
        # Load static prompt texts
        self.general_prompt = self._load_resource_file("resources/prompts/general.txt")
        self.application_preamble = self._load_resource_file("resources/prompts/application_preamble.txt")
        self.application_requirements = self._load_resource_file("resources/prompts/application_requirements.txt")
    
    def _load_resource_file(self, file_path: str) -> str:
        """
        Loads the content of a resource file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def generate(self, commands: List[Command], domain_model_files: DomainModelFiles) -> ApplicationFiles:
        """
        Generates application files based on the provided commands and domain model.
        """
        # Prepare system prompt
        system_prompt = (
            f"{self.application_preamble}\n\n"
            f"{self.general_prompt}\n\n"
            f"{self.message_parser.get_file_format_pattern()}\n\n"
            f"{self.application_requirements}"
        )
        
        # Prepare user prompt with commands and domain model files
        user_prompt = "Commands:\n"
        for cmd in commands:
            user_prompt += f"- {cmd.name}: {cmd.description}\n"
        
        user_prompt += "\nDomain Model Files:\n"
        for path, content in domain_model_files.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"
        
        # Create messages
        messages = [
            Message(role=MessageRole.SYSTEM, content=system_prompt),
            Message(role=MessageRole.USER, content=user_prompt)
        ]
        
        # Generate response using LLM
        response_message = self.llm_service.generate_response(messages)
        
        # Parse files from response
        files_dict = self.message_parser.parse_files_from_message(response_message)
        
        # Convert to ApplicationFiles
        application_files = ApplicationFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/application'):
                application_files.add_file(path, content)
        
        return application_files
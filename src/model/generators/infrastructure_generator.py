import os
from typing import List

from src.model.files.domain_model_files import DomainModelFiles
from src.model.files.infrastructure_files import InfrastructureFiles
from src.model.infrastructure_requirement.infrastructure_requirement import InfrastructureRequirement
from src.model.message.message import Message, MessageRole
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser


class InfrastructureGenerator:
    """
    Generator service that uses a LLM to generate infrastructure files based on requirements and domain model.
    """
    
    def __init__(self, llm_service: LLMService, message_parser: MessageParser):
        """
        Initializes the generator with the necessary services.
        """
        self.llm_service = llm_service
        self.message_parser = message_parser
        
        # Load static prompt texts
        self.general_prompt = self._load_resource_file("resources/prompts/general.txt")
        self.infrastructure_preamble = self._load_resource_file("resources/prompts/infrastructure_preamble.txt")
        self.infrastructure_requirements = self._load_resource_file("resources/prompts/infrastructure_requirements.txt")
    
    def _load_resource_file(self, file_path: str) -> str:
        """
        Loads the content of a resource file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def generate(self, infrastructure_requirements: List[InfrastructureRequirement], 
                domain_model_files: DomainModelFiles) -> InfrastructureFiles:
        """
        Generates infrastructure files based on the provided requirements and domain model.
        """
        # Prepare system prompt
        system_prompt = (
            f"{self.infrastructure_preamble}\n\n"
            f"{self.general_prompt}\n\n"
            f"{self.message_parser.get_file_format_pattern()}\n\n"
            f"{self.infrastructure_requirements}"
        )
        
        # Prepare user prompt with requirements and domain model files
        user_prompt = "Infrastructure Requirements:\n"
        for req in infrastructure_requirements:
            user_prompt += f"- {req.requirement_text}\n"
        
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
        
        # Convert to InfrastructureFiles
        infrastructure_files = InfrastructureFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/infrastructure'):
                infrastructure_files.add_file(path, content)
        
        return infrastructure_files
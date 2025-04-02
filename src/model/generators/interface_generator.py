import os

from src.model.files.application_files import ApplicationFiles
from src.model.files.domain_model_files import DomainModelFiles
from src.model.files.infrastructure_files import InfrastructureFiles
from src.model.files.interface_files import InterfaceFiles
from src.model.message.message import Message, MessageRole
from src.model.services.code_compressor import CodeCompressor
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser


class InterfaceGenerator:
    """
    Generator service that uses a LLM to generate interface files based on application, domain model, and infrastructure.
    """
    
    def __init__(self, llm_service: LLMService, message_parser: MessageParser, code_compressor: CodeCompressor):
        """
        Initializes the generator with the necessary services.
        """
        self.llm_service = llm_service
        self.message_parser = message_parser
        self.code_compressor = code_compressor
        
        # Load static prompt texts
        self.general_prompt = self._load_resource_file("resources/prompts/general.txt")
        self.interface_preamble = self._load_resource_file("resources/prompts/interface_preamble.txt")
        self.interface_requirements = self._load_resource_file("resources/prompts/interface_requirements.txt")
    
    def _load_resource_file(self, file_path: str) -> str:
        """
        Loads the content of a resource file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def generate(self, application_files: ApplicationFiles, domain_model_files: DomainModelFiles, 
                infrastructure_files: InfrastructureFiles) -> InterfaceFiles:
        """
        Generates interface files based on the provided application, domain model, and infrastructure files.
        """
        # Compress domain model and infrastructure files
        compressed_domain_model_files = self.code_compressor.compress(domain_model_files)
        compressed_infrastructure_files = self.code_compressor.compress(infrastructure_files)
        
        # Prepare system prompt
        system_prompt = (
            f"{self.interface_preamble}\n\n"
            f"{self.general_prompt}\n\n"
            f"{self.message_parser.get_file_format_pattern()}\n\n"
            f"{self.interface_requirements}"
        )
        
        # Prepare user prompt with application files and compressed domain model and infrastructure files
        user_prompt = "Application Files:\n"
        for path, content in application_files.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"
        
        user_prompt += "\nCompressed Domain Model Files:\n"
        for path, content in compressed_domain_model_files.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"
        
        user_prompt += "\nCompressed Infrastructure Files:\n"
        for path, content in compressed_infrastructure_files.get_all_files().items():
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
        
        # Convert to InterfaceFiles
        interface_files = InterfaceFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/interface'):
                interface_files.add_file(path, content)
        
        return interface_files
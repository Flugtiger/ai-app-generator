import logging
import os

from src.model.files.files_dictionary import FilesDictionary
from src.model.files.infrastructure_files import InfrastructureFiles
from src.model.files.interface_files import InterfaceFiles
from src.model.message.message import Message, MessageRole
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser

logger = logging.getLogger(__name__)


class ProjectGenerator:
    """
    Generator service that uses a LLM to generate project files based on infrastructure and interface files.
    """

    def __init__(self, llm_service: LLMService, message_parser: MessageParser):
        """
        Initializes the generator with the necessary services.
        """
        self.llm_service = llm_service
        self.message_parser = message_parser

        # Load static prompt texts
        self.general_prompt = self._load_resource_file("resources/prompts/general.txt")
        self.project_preamble = self._load_resource_file("resources/prompts/project_preamble.txt")
        self.project_requirements = self._load_resource_file("resources/prompts/project_requirements.txt")

    def _load_resource_file(self, file_path: str) -> str:
        """
        Loads the content of a resource file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_imports(self, file_content: str) -> str:
        """
        Extracts import statements from file content.
        """
        lines = file_content.split('\n')
        imports = []

        for line in lines:
            if 'import' in line and line.strip().startswith(('import', 'from')):
                imports.append(line)

        return '\n'.join(imports)

    def generate(self, infrastructure_files: InfrastructureFiles, interface_files: InterfaceFiles) -> FilesDictionary:
        """
        Generates project files based on the provided infrastructure and interface files.
        """
        # Extract import statements from infrastructure and interface files
        infrastructure_imports = FilesDictionary()
        for path, content in infrastructure_files.get_all_files().items():
            imports = self._extract_imports(content)
            if imports:
                infrastructure_imports.add_file(path, imports)

        interface_imports = FilesDictionary()
        for path, content in interface_files.get_all_files().items():
            imports = self._extract_imports(content)
            if imports:
                interface_imports.add_file(path, imports)

        # Prepare system prompt
        system_prompt = (
            f"{self.project_preamble}\n\n"
            f"{self.general_prompt}\n\n"
            f"{self.message_parser.get_file_format_pattern()}\n\n"
            f"{self.project_requirements}"
        )

        # Prepare user prompt with import statements
        user_prompt = "Infrastructure File Imports:\n"
        for path, content in infrastructure_imports.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"

        user_prompt += "\nInterface File Imports:\n"
        for path, content in interface_imports.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"

        # Create messages
        logger.warning("gen-project system prompt:\n%s", system_prompt)
        messages = [
            Message(role=MessageRole.SYSTEM, content=system_prompt),
            Message(role=MessageRole.USER, content=user_prompt)
        ]

        # Generate response using LLM
        response_message = self.llm_service.generate_response(messages)

        # Parse files from response
        project_files = self.message_parser.parse_files_from_message(response_message)

        return project_files

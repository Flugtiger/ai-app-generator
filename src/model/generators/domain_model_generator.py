import os
from typing import List

from src.model.files.domain_model_files import DomainModelFiles
from src.model.message.message import Message, MessageRole
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.services.llm_service import LLMService
from src.model.services.message_parser import MessageParser


class DomainModelGenerator:
    """
    Generator service that uses a LLM to generate domain model files based on requirements.
    """

    def __init__(self, llm_service: LLMService, message_parser: MessageParser):
        """
        Initializes the generator with the necessary services.
        """
        self.llm_service = llm_service
        self.message_parser = message_parser

        # Load static prompt texts
        self.general_prompt = self._load_resource_file("resources/prompts/general.txt")
        self.model_preamble = self._load_resource_file("resources/prompts/model_preamble.txt")
        self.model_preamble_incr = self._load_resource_file("resources/prompts/model_preamble_incr.txt")
        self.model_requirements = self._load_resource_file("resources/prompts/model_requirements.txt")

    def _load_resource_file(self, file_path: str) -> str:
        """
        Loads the content of a resource file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def generate(self, model_requirements: List[ModelRequirement]) -> DomainModelFiles:
        """
        Generates domain model files based on the provided requirements.
        """
        # Prepare system prompt
        system_prompt = (
            f"{self.model_preamble}\n\n"
            f"{self.general_prompt}\n\n"
            f"{self.message_parser.get_file_format_pattern()}\n\n"
            f"{self.model_requirements}"
        )

        # Prepare user prompt with requirements
        user_prompt = "The requirements:\n"
        for i, req in enumerate(model_requirements, 1):
            user_prompt += f"{req.requirement_text}\n"

        # Create messages
        messages = [
            Message(role=MessageRole.SYSTEM, content=system_prompt),
            Message(role=MessageRole.USER, content=user_prompt)
        ]

        # Generate response using LLM
        response_message = self.llm_service.generate_response(messages)

        # Parse files from response
        files_dict = self.message_parser.parse_files_from_message(response_message)

        # Convert to DomainModelFiles
        domain_model_files = DomainModelFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/model'):
                domain_model_files.add_file(path, content)

        return domain_model_files

    def implement(self, model_requirement: ModelRequirement, existing_domain_model: DomainModelFiles) -> DomainModelFiles:
        """
        Implements a single requirement in an existing domain model.
        """

        system_prompt = "\n\n".join([
            self.model_preamble_incr,
            self.general_prompt,
            self.message_parser.get_edit_format_pattern(),
            self.model_requirements
        ])

        user_prompt = "Existing Domain Model Files:\n"
        for path, content in existing_domain_model.get_all_files().items():
            user_prompt += f"\n{path}:\n```\n{content}\n```\n"

        user_prompt += "\n\nThe requirement to be implemented:\n"
        user_prompt += f"{model_requirement.id}: {model_requirement.requirement_text}"

        # Create messages
        messages = [
            Message(role=MessageRole.SYSTEM, content=system_prompt),
            Message(role=MessageRole.USER, content=user_prompt)
        ]

        # Generate response using LLM
        response_message = self.llm_service.generate_response(messages)

        # Parse files from response
        files_dict = self.message_parser.apply_edits_from_message(response_message, existing_domain_model)

        # Convert to DomainModelFiles
        domain_model_files = DomainModelFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/model'):
                domain_model_files.add_file(path, content)

        return domain_model_files

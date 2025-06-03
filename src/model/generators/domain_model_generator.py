import re
from typing import List

from src.model.model_requirement.model_requirement_id import ModelRequirementId
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
        for req in model_requirements:
            user_prompt += f"{req.id}: {req.requirement_text}\n"

        # Create messages
        messages = [
            Message(role=MessageRole.SYSTEM, content=system_prompt),
            Message(role=MessageRole.USER, content=user_prompt)
        ]

        # Generate response using LLM
        response_message = self.llm_service.generate_response(messages)

        # Parse files from response
        files_dict, requirement_to_files = self.message_parser.parse_files_from_message(response_message)

        # Convert to DomainModelFiles
        domain_model_files = DomainModelFiles()
        for path, content in files_dict.get_all_files().items():
            if path.startswith('src/model'):
                domain_model_files.add_file(path, content)

        # Mark requirements as implemented
        for req in model_requirements:
            req_id_str = str(req.id)
            if req_id_str in requirement_to_files:
                req.implement(requirement_to_files[req_id_str])

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

        user_prompt += "\n\nAfter implementing the requirement, please specify in which files it is implemented by writing:"
        user_prompt += "\n\"Requirement <requirement-id> is implemented in:\n- <file-path-1>\n- <file-path-2>\n...\""

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

        # Mark the requirement as implemented
        file_paths = self._get_file_paths_for_implemented_requirement(model_requirement, response_message)
        if file_paths:
            model_requirement.implement(file_paths)
        else:
            # Fallback: use all files if no specific files were mentioned
            model_requirement.implement(list(files_dict.get_all_files().keys()))

        return domain_model_files

    def _get_file_paths_for_implemented_requirement(self, requirement: ModelRequirement, msg: Message) -> List[str]:
        """
        Extracts the file paths where a requirement is implemented from the message content.

        Args:
            requirement: The requirement to look for
            msg: The message to parse

        Returns:
            A list of file paths where the requirement is implemented
        """
        req_id_str = str(requirement.id)
        file_paths = []

        # Look for patterns like "Requirement REQ001 is implemented in:" followed by a list
        pattern = rf"Requirement\s+{re.escape(req_id_str)}\s+is\s+implemented\s+in:\s*(?:\n\s*-\s*([^\n]+))+?"
        match = re.search(pattern, msg.content, re.IGNORECASE)

        if match:
            # Extract all file paths from the list
            list_pattern = rf"Requirement\s+{re.escape(req_id_str)}\s+is\s+implemented\s+in:(?:\s*\n\s*-\s*([^\n]+))+"
            file_matches = re.findall(r"-\s*([^\n]+)", msg.content[match.start():])
            file_paths.extend([path.strip() for path in file_matches])

        return file_paths

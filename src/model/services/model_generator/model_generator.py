from typing import List
import os
from pathlib import Path
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.value_objects.domain_model_files import DomainModelFiles
from src.model.services.llm_service import LlmService
from src.model.services.message_parser import MessageParser
from src.model.value_objects.message import Message

from logging import getLogger

logger = getLogger(__name__)


class ModelGenerator:
    """
    Domain service that generates DDD model code using a LLM.
    """

    def __init__(self, llm_service: LlmService):
        """
        Initialize the ModelGenerator with a LLM service.

        Args:
            llm_service: The LLM service to use for generating the model.
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
        prompts_dir = Path("resources/prompts")
        file_path = prompts_dir / filename

        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            # Return a default message if the file doesn't exist
            return f"Prompt file '{filename}' not found in {prompts_dir}"

    def generate_model(self, requirements: List[ModelRequirement]) -> DomainModelFiles:
        """
        Generates a DDD model from scratch based on the provided requirements.

        Args:
            requirements: The requirements for the DDD model.

        Returns:
            A DomainModel containing the generated code.
        """
        assert requirements, "Requirements cannot be empty"

        # Prepare the requirements text
        requirements_text = "\n".join([f"{req.id}: {req.requirement_text}" for req in requirements])

        # Load the system prompt from file and format it with requirements
        roadmap = self._load_prompt_from_file("model_preamble.txt")
        general_prompt = self._load_prompt_from_file("general.txt")
        philosophy = self._load_prompt_from_file("model_requirements.txt")
        system_prompt = "\n\n".join([
            roadmap,
            general_prompt,
            "The requirements:",
            requirements_text,
            self.message_parser.get_file_template_with_example(),
            philosophy])

        # Generate the model using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate a clean DDD model based on the requirements.")
        ]

        response = self.llm_service.generate_response(messages)
        logger.info("LLM response:\n%s", response.model_dump_json(indent=2))

        # Parse the files from the response
        files_dict = self.message_parser.parse_files_from_message(response)

        # Convert to DomainModel
        domain_model = DomainModelFiles(files=files_dict.files)

        return domain_model

    def modify_model(self, requirements: List[ModelRequirement], current_model: DomainModelFiles) -> DomainModelFiles:
        """
        Modifies an existing DDD model based on the provided requirements.

        Args:
            requirements: The requirements for the DDD model.
            current_model: The current domain model to modify.

        Returns:
            A DomainModel containing the modified code.
        """
        assert requirements, "Requirements cannot be empty"
        assert current_model, "Current model cannot be empty"

        # Prepare the requirements text
        requirements_text = "\n".join([f"{req.id}: {req.requirement_text}" for req in requirements])

        # Prepare the current model files
        current_files = ""
        for path, content in current_model.files.items():
            current_files += f"\n{path}\nSOF```\n{content}\n```EOF\n"

        # Load the system prompt from file and format it with requirements and current model
        roadmap = self._load_prompt_from_file("model_modifier_roadmap.txt")
        philosophy = self._load_prompt_from_file("model_philosophy.txt")
        system_prompt = "\n\n".join([
            roadmap,
            "The requirements:",
            requirements_text,
            "Here is the current model:",
            current_files,
            self.message_parser.get_diff_template_with_example(),
            philosophy])

        # Generate the model modifications using the LLM
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content="Please generate the necessary changes to the DDD model based on the requirements.")
        ]

        response = self.llm_service.generate_response(messages)

        # Parse the diffs from the response
        diffs = self.message_parser.parse_diffs_from_message(response)

        # Create a new domain model as a copy of the current one
        modified_model = DomainModelFiles(files=dict(current_model.files))

        # Apply the diffs to the model
        for filename, diff_content in diffs.items():
            modified_model.apply_diff(diff_content)

        return modified_model

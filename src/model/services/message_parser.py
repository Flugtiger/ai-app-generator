from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from src.model.files.files_dictionary import FilesDictionary
from src.model.message.message import Message
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class MessageParser(ABC):
    """
    Abstract domain service for parsing file contents from LLM response Messages.
    """

    @abstractmethod
    def get_file_format_pattern(self) -> str:
        """
        Returns a pattern for how to define files, including an example, for use in system prompts.
        """
        pass

    @abstractmethod
    def parse_files_from_message(self, message: Message) -> Tuple[FilesDictionary, Dict[str, List[str]]]:
        """
        Parses a LLM response message and returns a tuple containing:
        1. A FilesDictionary with the parsed files
        2. A dictionary mapping requirement IDs to lists of file paths that implement them
        """
        pass

    @abstractmethod
    def get_edit_format_pattern(self) -> str:
        """
        Returns a pattern for how to define file edits, including an example, for use in system prompts.
        """
        pass

    @abstractmethod
    def apply_edits_from_message(self, message: Message, files_dict: FilesDictionary) -> FilesDictionary:
        """
            Parses a LLM response message for file edits and applies them to the provided FilesDictionary.
            Returns the updated FilesDictionary
            """
        pass

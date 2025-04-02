from abc import ABC, abstractmethod

from src.model.files.files_dictionary import FilesDictionary
from src.model.message.message import Message


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
    def parse_files_from_message(self, message: Message) -> FilesDictionary:
        """
        Parses a LLM response message and returns a FilesDictionary with the parsed files.
        """
        pass
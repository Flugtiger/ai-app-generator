from abc import ABC, abstractmethod

from src.model.files.files_dictionary import FilesDictionary


class CodeCompressor(ABC):
    """
    Abstract domain service for compressing code files.
    """
    
    @abstractmethod
    def compress(self, files_dict: FilesDictionary) -> FilesDictionary:
        """
        Takes a FilesDictionary as parameter and returns a FilesDictionary where the file contents
        have been reduced to class declarations and constructor signatures.
        """
        pass
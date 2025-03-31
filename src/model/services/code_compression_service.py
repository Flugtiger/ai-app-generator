from abc import ABC, abstractmethod

from src.model.value_objects.files_dictionary import FilesDictionary


class CodeCompressionService(ABC):

    @abstractmethod
    def compress_to_constructor_signatures(self, files: FilesDictionary) -> FilesDictionary:
        """
        Compresses the given FilesDictionary so that only class declarations and constructor signatures are left in the source files.

        Args:
            files: A FilesDictionary with source code files.

        Returns:
            A FilesDictionary where only class declarations and constructor signatures are left in the contents of the files
        """
        pass

    @abstractmethod
    def remove_method_bodies(self, files: FilesDictionary) -> FilesDictionary:
        """
        Removes method bodies from the given FilesDictionary while keeping all other code intact.
        Method signatures, docstrings, and class definitions remain unchanged.

        Args:
            files: A FilesDictionary with source code files.

        Returns:
            A FilesDictionary where method bodies are replaced with 'pass' statements
        """
        pass

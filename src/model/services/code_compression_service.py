from abc import ABC, abstractmethod

from src.model.value_objects.files_dictionary import FilesDictionary


class CodeCompressionService(ABC):

    @abstractmethod
    def compress_to_constructor_signatures(files: FilesDictionary) -> FilesDictionary:
        """
        Compresses the given FilesDictionary so that only class declarations and constructor signatures are left in the source files.

        Args:
            files: A FilesDictionary with source code files.

        Returns:
            A FilesDictionary where only class declarations and constructor signatures are left in the contents of the files
        """
        pass

import re
from src.model.value_objects.files_dictionary import FilesDictionary


class DomainModelFiles(FilesDictionary):
    """
    A specialized FilesDictionary that represents a domain model's source code.
    All files in a DomainModel must be inside the 'src/model' directory.
    """

    def add_file(self, path: str, content: str) -> None:
        """
        Add a file to the domain model, ensuring it's inside the 'src/model' directory.

        Args:
            path: The path of the file relative to the project root.
            content: The content of the file.

        Raises:
            ValueError: If the path is not inside the 'src/model' directory.
        """
        if not path.startswith('src/model/'):
            raise ValueError(f"Domain model files must be inside 'src/model' directory, got: {path}")

        super().add_file(path, content)

    def merge(self, other: 'FilesDictionary') -> None:
        """
        Merges another FilesDictionary into this one, ensuring all files are inside 'src/model'.
        Files in the other dictionary will overwrite files in this one if they have the same path.

        Args:
            other: The FilesDictionary to merge into this one.

        Raises:
            ValueError: If any file in the other dictionary is not inside 'src/model'.
        """
        # Check that all files in the other dictionary are inside 'src/model'
        for path in other.files.keys():
            if not path.startswith('src/model/'):
                raise ValueError(f"Cannot merge file outside 'src/model' directory: {path}")

        # Merge the files
        super().merge(other)

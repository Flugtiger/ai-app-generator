from src.model.value_objects.files_dictionary import FilesDictionary


class InterfaceFiles(FilesDictionary):
    """
    A specialized FilesDictionary that represents interface code.
    All files in InterfaceFiles must be inside the 'src/interface' directory.
    """

    def add_file(self, path: str, content: str) -> None:
        """
        Add a file to the interface files, ensuring it's inside the 'src/interface' directory.

        Args:
            path: The path of the file relative to the project root.
            content: The content of the file.

        Raises:
            ValueError: If the path is not inside the 'src/interface' directory.
        """
        if not path.startswith('src/interface/'):
            raise ValueError(f"Interface files must be inside 'src/interface' directory, got: {path}")

        super().add_file(path, content)

    def merge(self, other: 'FilesDictionary') -> None:
        """
        Merges another FilesDictionary into this one, ensuring all files are inside 'src/interface'.
        Files in the other dictionary will overwrite files in this one if they have the same path.

        Args:
            other: The FilesDictionary to merge into this one.

        Raises:
            ValueError: If any file in the other dictionary is not inside 'src/interface'.
        """
        # Check that all files in the other dictionary are inside 'src/interface'
        for path in other.files.keys():
            if not path.startswith('src/interface/'):
                raise ValueError(f"Cannot merge file outside 'src/interface' directory: {path}")

        # Merge the files
        super().merge(other)

from src.model.value_objects.files_dictionary import FilesDictionary


class InfrastructureFiles(FilesDictionary):
    """
    A specialized FilesDictionary that represents infrastructure code.
    All files in InfrastructureFiles must be inside the 'src/infrastructure' directory.
    """

    def add_file(self, path: str, content: str) -> None:
        """
        Add a file to the infrastructure files, ensuring it's inside the 'src/infrastructure' directory.

        Args:
            path: The path of the file relative to the project root.
            content: The content of the file.

        Raises:
            ValueError: If the path is not inside the 'src/infrastructure' directory.
        """
        if not path.startswith('src/infrastructure/'):
            raise ValueError(f"Infrastructure files must be inside 'src/infrastructure' directory, got: {path}")

        super().add_file(path, content)

    def merge(self, other: 'FilesDictionary') -> None:
        """
        Merges another FilesDictionary into this one, ensuring all files are inside 'src/infrastructure'.
        Files in the other dictionary will overwrite files in this one if they have the same path.

        Args:
            other: The FilesDictionary to merge into this one.

        Raises:
            ValueError: If any file in the other dictionary is not inside 'src/infrastructure'.
        """
        # Check that all files in the other dictionary are inside 'src/infrastructure'
        for path in other.files.keys():
            if not path.startswith('src/infrastructure/'):
                raise ValueError(f"Cannot merge file outside 'src/infrastructure' directory: {path}")

        # Merge the files
        super().merge(other)

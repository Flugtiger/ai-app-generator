from pathlib import Path
from typing import List, Optional, TypeVar, Generic, Type

from src.model.value_objects.files_dictionary import FilesDictionary
from src.model.services.files_dictionary_service import FilesDictionaryService

T = TypeVar('T', bound=FilesDictionary)


class BaseFilesService(Generic[T]):
    """
    Base service for reading and writing specialized FilesDictionary objects from/to a file system.
    """

    def __init__(self, directory_name: str, file_class: Type[T]):
        """
        Initialize the service with configuration.

        Args:
            directory_name: The name of the directory within src/ to read from/write to.
            file_class: The class to instantiate for the result.
        """
        self.directory_name = directory_name
        self.file_class = file_class
        self.default_ignore_patterns = ['__pycache__', '*.pyc', '.git', '.vscode', '.idea']

    def read_from_directory(self, project_root: str, ignore_patterns: Optional[List[str]] = None) -> T:
        """
        Reads files from a directory, including only files inside the specified directory.

        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').

        Returns:
            A specialized FilesDictionary containing all files from the directory.
        """
        if ignore_patterns is None:
            ignore_patterns = self.default_ignore_patterns

        # Create the path to the specified directory
        target_dir = Path(project_root) / 'src' / self.directory_name

        # Check if the directory exists
        if not target_dir.exists() or not target_dir.is_dir():
            # Return an empty instance if the directory doesn't exist
            return self.file_class()

        # Read only files from the specified directory
        files_dict = FilesDictionaryService.read_from_directory(str(target_dir), ignore_patterns)

        # Create a new instance of the specialized FilesDictionary
        result = self.file_class()

        # Add files with corrected paths
        for path, content in files_dict.files.items():
            # Prepend 'src/{directory_name}/' to the path
            full_path = f"src/{self.directory_name}/{path}"
            try:
                result.add_file(full_path, content)
            except ValueError as e:
                print(f"Warning: {e}")

        return result

    def write_to_directory(self, files: FilesDictionary, project_root: str, create_dirs: bool = True) -> None:
        """
        Writes a specialized FilesDictionary to a directory.

        Args:
            files: The specialized FilesDictionary to write.
            project_root: The root directory of the project.
            create_dirs: Whether to create directories if they don't exist.
        """
        # Write the files to the directory
        FilesDictionaryService.write_to_directory(files, project_root, create_dirs)

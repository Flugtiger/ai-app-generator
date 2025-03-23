from typing import List, Optional

from src.model.value_objects.application_files import ApplicationFiles
from src.model.services.base_files_service import BaseFilesService


class ApplicationFilesService(BaseFilesService[ApplicationFiles]):
    """
    Service for reading and writing ApplicationFiles objects from/to a file system.
    """

    @classmethod
    def read_from_directory(cls, project_root: str, ignore_patterns: Optional[List[str]] = None) -> ApplicationFiles:
        """
        Reads an ApplicationFiles from a directory, including only files inside 'src/application'.

        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').

        Returns:
            An ApplicationFiles containing all application service files from the directory.
        """
        return super().read_from_directory(project_root, 'application', ApplicationFiles, ignore_patterns)

    @staticmethod
    def create_empty_application_files() -> ApplicationFiles:
        """
        Creates an empty ApplicationFiles.

        Returns:
            An empty ApplicationFiles.
        """
        return ApplicationFiles()

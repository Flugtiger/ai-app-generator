from typing import List, Optional

from src.model.value_objects.infrastructure_files import InfrastructureFiles
from src.model.services.base_files_service import BaseFilesService


class InfrastructureFilesService(BaseFilesService[InfrastructureFiles]):
    """
    Service for reading and writing InfrastructureFiles objects from/to a file system.
    """

    @classmethod
    def read_from_directory(cls, project_root: str, ignore_patterns: Optional[List[str]] = None) -> InfrastructureFiles:
        """
        Reads an InfrastructureFiles from a directory, including only files inside 'src/infrastructure'.

        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').

        Returns:
            An InfrastructureFiles containing all infrastructure files from the directory.
        """
        return super().read_from_directory(project_root, 'infrastructure', InfrastructureFiles, ignore_patterns)

    @staticmethod
    def create_empty_infrastructure_files() -> InfrastructureFiles:
        """
        Creates an empty InfrastructureFiles.

        Returns:
            An empty InfrastructureFiles.
        """
        return InfrastructureFiles()

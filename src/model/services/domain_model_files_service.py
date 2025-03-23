from typing import List, Optional

from src.model.value_objects.domain_model_files import DomainModelFiles
from src.model.services.base_files_service import BaseFilesService


class DomainModelFilesService(BaseFilesService[DomainModelFiles]):
    """
    Service for reading and writing DomainModel objects from/to a file system.
    """

    @classmethod
    def read_from_directory(cls, project_root: str, ignore_patterns: Optional[List[str]] = None) -> DomainModelFiles:
        """
        Reads a DomainModel from a directory, including only files inside 'src/model'.

        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').

        Returns:
            A DomainModel containing all model files from the directory.
        """
        return super().read_from_directory(project_root, 'model', DomainModelFiles, ignore_patterns)

    @staticmethod
    def create_empty_domain_model() -> DomainModelFiles:
        """
        Creates an empty DomainModel.

        Returns:
            An empty DomainModel.
        """
        return DomainModelFiles()

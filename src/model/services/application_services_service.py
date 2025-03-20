from pathlib import Path
from typing import List, Optional

from src.model.value_objects.application_services import ApplicationFiles
from src.model.services.files_dictionary_service import FilesDictionaryService


class ApplicationServicesService:
    """
    Service for reading and writing ApplicationServices objects from/to a file system.
    """

    @staticmethod
    def read_from_directory(project_root: str, ignore_patterns: Optional[List[str]] = None) -> ApplicationFiles:
        """
        Reads an ApplicationServices from a directory, including only files inside 'src/application'.

        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').

        Returns:
            An ApplicationServices containing all application service files from the directory.
        """
        if ignore_patterns is None:
            ignore_patterns = ['__pycache__', '*.pyc', '.git', '.vscode', '.idea']

        # Create the path to the application directory
        app_dir = Path(project_root) / 'src' / 'application'

        # Check if the application directory exists
        if not app_dir.exists() or not app_dir.is_dir():
            # Return an empty application services if the directory doesn't exist
            return ApplicationFiles()

        # Read only files from the application directory
        files_dict = FilesDictionaryService.read_from_directory(str(app_dir), ignore_patterns)

        # Create a new ApplicationServices
        app_services = ApplicationFiles()

        # Add files to the application services with corrected paths
        for path, content in files_dict.files.items():
            # Prepend 'src/application/' to the path
            app_path = f"src/application/{path}"
            try:
                app_services.add_file(app_path, content)
            except ValueError as e:
                print(f"Warning: {e}")

        return app_services

    @staticmethod
    def write_to_directory(app_services: ApplicationFiles, project_root: str, create_dirs: bool = True) -> None:
        """
        Writes an ApplicationServices to a directory.

        Args:
            app_services: The ApplicationServices to write.
            project_root: The root directory of the project.
            create_dirs: Whether to create directories if they don't exist.
        """
        # Write the application services to the directory
        FilesDictionaryService.write_to_directory(app_services, project_root, create_dirs)

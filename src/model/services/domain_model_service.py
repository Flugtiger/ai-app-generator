from pathlib import Path
from typing import List, Optional

from src.model.value_objects.domain_model import DomainModel
from src.model.services.files_dictionary_service import FilesDictionaryService


class DomainModelService:
    """
    Service for reading and writing DomainModel objects from/to a file system.
    """
    
    @staticmethod
    def read_from_directory(project_root: str, ignore_patterns: Optional[List[str]] = None) -> DomainModel:
        """
        Reads a DomainModel from a directory, including only files inside 'src/model'.
        
        Args:
            project_root: The root directory of the project.
            ignore_patterns: Optional list of patterns to ignore (e.g., '*.pyc', '__pycache__').
            
        Returns:
            A DomainModel containing all model files from the directory.
        """
        if ignore_patterns is None:
            ignore_patterns = ['__pycache__', '*.pyc', '.git', '.vscode', '.idea']
        
        # Create the path to the model directory
        model_dir = Path(project_root) / 'src' / 'model'
        
        # Check if the model directory exists
        if not model_dir.exists() or not model_dir.is_dir():
            # Return an empty domain model if the directory doesn't exist
            return DomainModel()
        
        # Read only files from the model directory
        files_dict = FilesDictionaryService.read_from_directory(str(model_dir), ignore_patterns)
        
        # Create a new DomainModel
        domain_model = DomainModel()
        
        # Add files to the domain model with corrected paths
        for path, content in files_dict.files.items():
            # Prepend 'src/model/' to the path
            model_path = f"src/model/{path}"
            try:
                domain_model.add_file(model_path, content)
            except ValueError as e:
                print(f"Warning: {e}")
        
        return domain_model
    
    @staticmethod
    def write_to_directory(domain_model: DomainModel, project_root: str, create_dirs: bool = True) -> None:
        """
        Writes a DomainModel to a directory.
        
        Args:
            domain_model: The DomainModel to write.
            project_root: The root directory of the project.
            create_dirs: Whether to create directories if they don't exist.
        """
        # Validate the domain model
        if not domain_model.validate():
            raise ValueError("Cannot write invalid domain model to directory")
        
        # Write the domain model to the directory
        FilesDictionaryService.write_to_directory(domain_model, project_root, create_dirs)
    
    @staticmethod
    def create_empty_domain_model() -> DomainModel:
        """
        Creates an empty DomainModel.
        
        Returns:
            An empty DomainModel.
        """
        return DomainModel()

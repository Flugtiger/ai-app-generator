from src.model.files.infrastructure_files import InfrastructureFiles
from src.model.services.base_files_service import BaseFilesService


class InfrastructureFilesService(BaseFilesService):
    """
    Concrete BaseFilesService for reading and writing InfrastructureFiles.
    """
    
    def __init__(self):
        """
        Initializes the service with the 'src/infrastructure' subfolder and InfrastructureFiles class.
        """
        super().__init__('src/infrastructure', InfrastructureFiles)
    
    def read_files(self, project_root_path: str) -> InfrastructureFiles:
        """
        Reads all files inside the 'src/infrastructure' subfolder into an InfrastructureFiles object.
        """
        return super().read_files(project_root_path)
    
    def write_files(self, project_root_path: str, files_dict: InfrastructureFiles) -> None:
        """
        Writes the files from the InfrastructureFiles to the 'src/infrastructure' subfolder.
        """
        super().write_files(project_root_path, files_dict)
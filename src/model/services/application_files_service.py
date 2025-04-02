from src.model.files.application_files import ApplicationFiles
from src.model.services.base_files_service import BaseFilesService


class ApplicationFilesService(BaseFilesService):
    """
    Concrete BaseFilesService for reading and writing ApplicationFiles.
    """
    
    def __init__(self):
        """
        Initializes the service with the 'src/application' subfolder and ApplicationFiles class.
        """
        super().__init__('src/application', ApplicationFiles)
    
    def read_files(self, project_root_path: str) -> ApplicationFiles:
        """
        Reads all files inside the 'src/application' subfolder into an ApplicationFiles object.
        """
        return super().read_files(project_root_path)
    
    def write_files(self, project_root_path: str, files_dict: ApplicationFiles) -> None:
        """
        Writes the files from the ApplicationFiles to the 'src/application' subfolder.
        """
        super().write_files(project_root_path, files_dict)
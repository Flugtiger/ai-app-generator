from src.model.files.domain_model_files import DomainModelFiles
from src.model.services.base_files_service import BaseFilesService


class DomainModelFilesService(BaseFilesService):
    """
    Concrete BaseFilesService for reading and writing DomainModelFiles.
    """
    
    def __init__(self):
        """
        Initializes the service with the 'src/model' subfolder and DomainModelFiles class.
        """
        super().__init__('src/model', DomainModelFiles)
    
    def read_files(self, project_root_path: str) -> DomainModelFiles:
        """
        Reads all files inside the 'src/model' subfolder into a DomainModelFiles object.
        """
        return super().read_files(project_root_path)
    
    def write_files(self, project_root_path: str, files_dict: DomainModelFiles) -> None:
        """
        Writes the files from the DomainModelFiles to the 'src/model' subfolder.
        """
        super().write_files(project_root_path, files_dict)
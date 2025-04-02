from src.model.files.interface_files import InterfaceFiles
from src.model.services.base_files_service import BaseFilesService


class InterfaceFilesService(BaseFilesService):
    """
    Concrete BaseFilesService for reading and writing InterfaceFiles.
    """
    
    def __init__(self):
        """
        Initializes the service with the 'src/interface' subfolder and InterfaceFiles class.
        """
        super().__init__('src/interface', InterfaceFiles)
    
    def read_files(self, project_root_path: str) -> InterfaceFiles:
        """
        Reads all files inside the 'src/interface' subfolder into an InterfaceFiles object.
        """
        return super().read_files(project_root_path)
    
    def write_files(self, project_root_path: str, files_dict: InterfaceFiles) -> None:
        """
        Writes the files from the InterfaceFiles to the 'src/interface' subfolder.
        """
        super().write_files(project_root_path, files_dict)
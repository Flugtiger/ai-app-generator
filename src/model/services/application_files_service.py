from typing import List, Optional

from src.model.value_objects.application_files import ApplicationFiles
from src.model.services.base_files_service import BaseFilesService


class ApplicationFilesService(BaseFilesService[ApplicationFiles]):
    """
    Service for reading and writing ApplicationFiles objects from/to a file system.
    """

    def __init__(self):
        """
        Initialize the service with application files configuration.
        """
        super().__init__('application', ApplicationFiles)

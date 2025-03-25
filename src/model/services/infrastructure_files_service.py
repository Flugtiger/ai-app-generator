from typing import List, Optional

from src.model.value_objects.infrastructure_files import InfrastructureFiles
from src.model.services.base_files_service import BaseFilesService


class InfrastructureFilesService(BaseFilesService[InfrastructureFiles]):
    """
    Service for reading and writing InfrastructureFiles objects from/to a file system.
    """

    def __init__(self):
        """
        Initialize the service with infrastructure files configuration.
        """
        super().__init__('infrastructure', InfrastructureFiles)

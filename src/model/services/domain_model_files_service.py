from typing import List, Optional

from src.model.value_objects.domain_model_files import DomainModelFiles
from src.model.services.base_files_service import BaseFilesService


class DomainModelFilesService(BaseFilesService[DomainModelFiles]):
    """
    Service for reading and writing DomainModel objects from/to a file system.
    """

    def __init__(self):
        """
        Initialize the service with domain model configuration.
        """
        super().__init__('model', DomainModelFiles)

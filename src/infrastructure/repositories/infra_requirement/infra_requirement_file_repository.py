import os
from pathlib import Path
from typing import List, Optional, Type

from src.infrastructure.repositories.file_based_repository import FileBasedRepository
from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.infra_requirement.infra_requirement_id import InfraRequirementId
from src.model.infra_requirement.infra_requirement_repository import InfraRequirementRepository


class InfraRequirementFileRepository(FileBasedRepository[InfraRequirement, InfraRequirementId], InfraRequirementRepository):
    """
    File-based implementation of the InfraRequirementRepository.
    """

    def __init__(self, base_dir: str = "data/infra_requirements"):
        """
        Initialize the repository with a base directory for storing infra requirement files.

        Args:
            base_dir: The base directory where model requirement files will be stored
        """
        super().__init__(base_dir)

    def get_id(self, entity: InfraRequirement) -> InfraRequirementId:
        """
        Extract the ID from a InfraRequirement entity.

        Args:
            entity: The InfraRequirement to extract the ID from

        Returns:
            The ID of the InfraRequirement
        """
        return entity.id

    def get_entity_type(self) -> Type[InfraRequirement]:
        """
        Get the type of entity this repository manages.

        Returns:
            The InfraRequirement type
        """
        return InfraRequirement

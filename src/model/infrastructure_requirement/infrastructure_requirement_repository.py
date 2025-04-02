from abc import ABC, abstractmethod
from typing import List

from src.model.infrastructure_requirement.infrastructure_requirement import InfrastructureRequirement
from src.model.infrastructure_requirement.infrastructure_requirement_id import InfrastructureRequirementId


class InfrastructureRequirementRepository(ABC):
    """
    Repository interface for InfrastructureRequirement aggregate.
    """
    @abstractmethod
    def get_by_id(self, id: InfrastructureRequirementId) -> InfrastructureRequirement:
        """
        Retrieves an InfrastructureRequirement by its ID.
        """
        pass

    @abstractmethod
    def save(self, infrastructure_requirement: InfrastructureRequirement) -> InfrastructureRequirement:
        """
        Saves an InfrastructureRequirement to the repository.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[InfrastructureRequirement]:
        """
        Retrieves all InfrastructureRequirements from the repository.
        """
        pass
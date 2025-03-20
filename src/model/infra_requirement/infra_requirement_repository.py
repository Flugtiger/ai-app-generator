from abc import ABC, abstractmethod
from typing import Optional
from src.model.infra_requirement.infra_requirement import InfraRequirement
from src.model.infra_requirement.infra_requirement_id import InfraRequirementId


class InfraRequirementRepository(ABC):
    """
    Repository interface for InfraRequirement entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: InfraRequirementId) -> Optional[InfraRequirement]:
        """
        Retrieves an InfraRequirement by its ID.
        
        Args:
            id: The ID of the InfraRequirement to retrieve.
            
        Returns:
            The InfraRequirement if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def save(self, infra_requirement: InfraRequirement) -> None:
        """
        Saves an InfraRequirement to the repository.
        
        Args:
            infra_requirement: The InfraRequirement to save.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[InfraRequirement]:
        """
        Retrieves all InfraRequirements from the repository.
        
        Returns:
            A list of all InfraRequirements.
        """
        pass

from abc import ABC, abstractmethod
from typing import Optional
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirementRepository(ABC):
    """
    Repository interface for ModelRequirement entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: ModelRequirementId) -> Optional[ModelRequirement]:
        """
        Retrieves a ModelRequirement by its ID.
        
        Args:
            id: The ID of the ModelRequirement to retrieve.
            
        Returns:
            The ModelRequirement if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def save(self, model_requirement: ModelRequirement) -> None:
        """
        Saves a ModelRequirement to the repository.
        
        Args:
            model_requirement: The ModelRequirement to save.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[ModelRequirement]:
        """
        Retrieves all ModelRequirements from the repository.
        
        Returns:
            A list of all ModelRequirements.
        """
        pass
from abc import ABC, abstractmethod
from typing import Optional, List

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.bounded_context.bounded_context_id import BoundedContextId


class ModelRequirementRepository(ABC):
    """
    Repository interface for ModelRequirement entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: ModelRequirementId) -> Optional[ModelRequirement]:
        """
        Retrieves a ModelRequirement by its ID.
        
        Args:
            id: ID of the ModelRequirement to retrieve
            
        Returns:
            The ModelRequirement if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save(self, model_requirement: ModelRequirement) -> None:
        """
        Saves a ModelRequirement to the repository.
        
        Args:
            model_requirement: ModelRequirement to save
        """
        pass
    
    @abstractmethod
    def get_by_bounded_context_id(self, bounded_context_id: BoundedContextId) -> List[ModelRequirement]:
        """
        Retrieves all ModelRequirements for a given BoundedContext.
        
        Args:
            bounded_context_id: ID of the BoundedContext
            
        Returns:
            List of ModelRequirements for the BoundedContext
        """
        pass
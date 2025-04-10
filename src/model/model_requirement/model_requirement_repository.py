from abc import ABC, abstractmethod
from typing import List

from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId


class ModelRequirementRepository(ABC):
    """
    Repository interface for ModelRequirement aggregate.
    """
    @abstractmethod
    def get_by_id(self, id: ModelRequirementId) -> ModelRequirement:
        """
        Retrieves a ModelRequirement by its ID.
        """
        pass

    @abstractmethod
    def save(self, model_requirement: ModelRequirement) -> ModelRequirement:
        """
        Saves a ModelRequirement to the repository.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[ModelRequirement]:
        """
        Retrieves all ModelRequirements from the repository.
        """
        pass
        
    @abstractmethod
    def get_unimplemented(self) -> List[ModelRequirement]:
        """
        Retrieves all unimplemented ModelRequirements from the repository.
        """
        pass

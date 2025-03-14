import os
from pathlib import Path
from typing import List, Optional, Type

from src.infrastructure.repositories.file_based_repository import FileBasedRepository
from src.model.model_requirement.model_requirement import ModelRequirement
from src.model.model_requirement.model_requirement_id import ModelRequirementId
from src.model.model_requirement.model_requirement_repository import ModelRequirementRepository


class ModelRequirementFileRepository(FileBasedRepository[ModelRequirement, ModelRequirementId], ModelRequirementRepository):
    """
    File-based implementation of the ModelRequirementRepository.
    """
    
    def __init__(self, base_dir: str = "data/model_requirements"):
        """
        Initialize the repository with a base directory for storing model requirement files.
        
        Args:
            base_dir: The base directory where model requirement files will be stored
        """
        super().__init__(base_dir)
    
    def get_id(self, entity: ModelRequirement) -> ModelRequirementId:
        """
        Extract the ID from a ModelRequirement entity.
        
        Args:
            entity: The ModelRequirement to extract the ID from
            
        Returns:
            The ID of the ModelRequirement
        """
        return entity.id
    
    def get_entity_type(self) -> Type[ModelRequirement]:
        """
        Get the type of entity this repository manages.
        
        Returns:
            The ModelRequirement type
        """
        return ModelRequirement
    
    def get_by_id(self, id: ModelRequirementId) -> Optional[ModelRequirement]:
        """
        Retrieves a ModelRequirement by its ID.
        
        Args:
            id: ID of the ModelRequirement to retrieve
            
        Returns:
            The ModelRequirement if found, None otherwise
        """
        return super().get_by_id(id)
    
    def save(self, model_requirement: ModelRequirement) -> None:
        """
        Saves a ModelRequirement to the repository.
        
        Args:
            model_requirement: ModelRequirement to save
        """
        super().save(model_requirement)
    
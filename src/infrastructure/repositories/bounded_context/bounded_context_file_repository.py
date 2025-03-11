import os
from pathlib import Path
from typing import Optional, Type

from src.infrastructure.repositories.file_based_repository import FileBasedRepository
from src.model.bounded_context.bounded_context import BoundedContext
from src.model.bounded_context.bounded_context_id import BoundedContextId
from src.model.bounded_context.bounded_context_repository import BoundedContextRepository


class BoundedContextFileRepository(FileBasedRepository[BoundedContext, BoundedContextId], BoundedContextRepository):
    """
    File-based implementation of the BoundedContextRepository.
    """
    
    def __init__(self, base_dir: str = "data/bounded_contexts"):
        """
        Initialize the repository with a base directory for storing bounded context files.
        
        Args:
            base_dir: The base directory where bounded context files will be stored
        """
        super().__init__(base_dir)
    
    def get_id(self, entity: BoundedContext) -> BoundedContextId:
        """
        Extract the ID from a BoundedContext entity.
        
        Args:
            entity: The BoundedContext to extract the ID from
            
        Returns:
            The ID of the BoundedContext
        """
        return entity.id
    
    def get_entity_type(self) -> Type[BoundedContext]:
        """
        Get the type of entity this repository manages.
        
        Returns:
            The BoundedContext type
        """
        return BoundedContext
    
    def get_by_id(self, id: BoundedContextId) -> Optional[BoundedContext]:
        """
        Retrieves a BoundedContext by its ID.
        
        Args:
            id: ID of the BoundedContext to retrieve
            
        Returns:
            The BoundedContext if found, None otherwise
        """
        return super().get_by_id(id)
    
    def save(self, bounded_context: BoundedContext) -> None:
        """
        Saves a BoundedContext to the repository.
        
        Args:
            bounded_context: BoundedContext to save
        """
        super().save(bounded_context)

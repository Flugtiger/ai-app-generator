from abc import ABC, abstractmethod
from typing import Optional

from src.model.bounded_context.bounded_context import BoundedContext
from src.model.bounded_context.bounded_context_id import BoundedContextId


class BoundedContextRepository(ABC):
    """
    Repository interface for BoundedContext entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: BoundedContextId) -> Optional[BoundedContext]:
        """
        Retrieves a BoundedContext by its ID.
        
        Args:
            id: ID of the BoundedContext to retrieve
            
        Returns:
            The BoundedContext if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save(self, bounded_context: BoundedContext) -> None:
        """
        Saves a BoundedContext to the repository.
        
        Args:
            bounded_context: BoundedContext to save
        """
        pass
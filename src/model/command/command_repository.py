from abc import ABC, abstractmethod
from typing import Optional, List

from src.model.command.command import Command
from src.model.command.command_id import CommandId
from src.model.bounded_context.bounded_context_id import BoundedContextId


class CommandRepository(ABC):
    """
    Repository interface for Command entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: CommandId) -> Optional[Command]:
        """
        Retrieves a Command by its ID.
        
        Args:
            id: ID of the Command to retrieve
            
        Returns:
            The Command if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save(self, command: Command) -> None:
        """
        Saves a Command to the repository.
        
        Args:
            command: Command to save
        """
        pass
    
    @abstractmethod
    def get_by_bounded_context_id(self, bounded_context_id: BoundedContextId) -> List[Command]:
        """
        Retrieves all Commands for a given BoundedContext.
        
        Args:
            bounded_context_id: ID of the BoundedContext
            
        Returns:
            List of Commands for the BoundedContext
        """
        pass
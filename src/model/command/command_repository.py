from abc import ABC, abstractmethod
from typing import Optional
from src.model.command.command import Command
from src.model.command.command_id import CommandId


class CommandRepository(ABC):
    """
    Repository interface for Command entities.
    """
    
    @abstractmethod
    def get_by_id(self, id: CommandId) -> Optional[Command]:
        """
        Retrieves a Command by its ID.
        
        Args:
            id: The ID of the Command to retrieve.
            
        Returns:
            The Command if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def save(self, command: Command) -> None:
        """
        Saves a Command to the repository.
        
        Args:
            command: The Command to save.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[Command]:
        """
        Retrieves all Commands from the repository.
        
        Returns:
            A list of all Commands.
        """
        pass
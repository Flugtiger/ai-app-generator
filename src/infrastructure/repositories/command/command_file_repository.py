import os
from pathlib import Path
from typing import List, Optional, Type

from src.infrastructure.repositories.file_based_repository import FileBasedRepository
from src.model.command.command import Command
from src.model.command.command_id import CommandId
from src.model.command.command_repository import CommandRepository


class CommandFileRepository(FileBasedRepository[Command, CommandId], CommandRepository):
    """
    File-based implementation of the CommandRepository.
    """
    
    def __init__(self, base_dir: str = "data/commands"):
        """
        Initialize the repository with a base directory for storing command files.
        
        Args:
            base_dir: The base directory where command files will be stored
        """
        super().__init__(base_dir)
    
    def get_id(self, entity: Command) -> CommandId:
        """
        Extract the ID from a Command entity.
        
        Args:
            entity: The Command to extract the ID from
            
        Returns:
            The ID of the Command
        """
        return entity.id
    
    def get_entity_type(self) -> Type[Command]:
        """
        Get the type of entity this repository manages.
        
        Returns:
            The Command type
        """
        return Command
    
    def get_by_id(self, id: CommandId) -> Optional[Command]:
        """
        Retrieves a Command by its ID.
        
        Args:
            id: ID of the Command to retrieve
            
        Returns:
            The Command if found, None otherwise
        """
        return super().get_by_id(id)
    
    def save(self, command: Command) -> None:
        """
        Saves a Command to the repository.
        
        Args:
            command: Command to save
        """
        super().save(command)
    

from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

from src.model.command.command import Command
from src.model.command.command_id import CommandId
from src.model.command.command_repository import CommandRepository


class CreateCommandInput(BaseModel):
    """
    Input data for creating a new command.
    """
    name: str
    description: str


class CreateCommandOutput(BaseModel):
    """
    Output data after creating a new command.
    """
    id: str
    name: str
    description: str


class CommandCommands:
    """
    Application service for command-related operations.
    """
    
    def __init__(self, command_repository: CommandRepository):
        """
        Initialize the CommandCommands service.
        
        Args:
            command_repository: Repository for Command entities
        """
        self.command_repository = command_repository
    
    def create_command(self, input_data: CreateCommandInput) -> CreateCommandOutput:
        """
        Create a new command with the given name and description.
        
        Args:
            input_data: Input data containing name and description
            
        Returns:
            Output data containing the created command's details
        """
        # Generate a unique ID for the command
        command_id = CommandId(value=f"CMD-{str(uuid4())}")
        
        # Create the command entity
        command = Command(
            id=command_id,
            name=input_data.name,
            description=input_data.description
        )
        
        # Save the command to the repository
        self.command_repository.save(command)
        
        # Return the output data
        return CreateCommandOutput(
            id=command.id.value,
            name=command.name,
            description=command.description
        )

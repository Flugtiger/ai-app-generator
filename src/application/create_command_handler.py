from pydantic import BaseModel, Field
from typing import Optional

from src.model.command.command import Command
from src.model.command.command_id import CommandId
from src.model.command.command_repository import CommandRepository


class CreateCommandInput(BaseModel):
    """
    Input DTO for creating a command
    """
    name: str = Field(..., description="The name of the command")
    description: str = Field(..., description="The description of the command")


class CreateCommandOutput(BaseModel):
    """
    Output DTO containing the ID of the created command
    """
    commandId: str


class CreateCommandHandler:
    """
    Handler for creating a new command
    """
    
    def __init__(self, command_repository: CommandRepository):
        """
        Initialize the handler with required dependencies
        """
        self.command_repository = command_repository
    
    def handle(self, input_dto: CreateCommandInput) -> CreateCommandOutput:
        """
        Creates a new command with the given name and description
        """
        # Create a new command
        command = Command(
            name=input_dto.name,
            description=input_dto.description
        )
        
        # Save the command to the repository
        saved_command = self.command_repository.save(command)
        
        # Return the ID of the created command
        return CreateCommandOutput(
            commandId=str(saved_command.id.value)
        )
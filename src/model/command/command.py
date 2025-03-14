from pydantic import BaseModel
from uuid import uuid4
from src.model.command.command_id import CommandId


class Command(BaseModel):
    """
    Represents a specific type of interaction in the software system.
    Has a name and description that can be modified after creation.
    """
    id: CommandId
    name: str
    description: str

    def __init__(self, **data):
        """
        Initialize a new Command.
        If no ID is provided, a new one will be generated.
        """
        if 'id' not in data:
            data['id'] = CommandId(str(uuid4()))
        
        super().__init__(**data)
    
    def update_name(self, new_name: str) -> None:
        """
        Updates the name of the command.
        
        Args:
            new_name: The new name for the command.
        """
        assert new_name, "Command name cannot be empty"
        self.name = new_name
    
    def update_description(self, new_description: str) -> None:
        """
        Updates the description of the command.
        
        Args:
            new_description: The new description for the command.
        """
        assert new_description, "Command description cannot be empty"
        self.description = new_description

    class Config:
        arbitrary_types_allowed = True